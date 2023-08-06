""" Run Input """
from __future__ import annotations

import logging
import warnings
from dataclasses import asdict, dataclass, field, fields
from http import HTTPStatus
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml

from mcli.api.exceptions import MAPIException
from mcli.api.schema.generic_model import DeserializableModel
from mcli.models.mcli_platform import MCLIPlatform
from mcli.serverside.platforms.platform_instances import (IncompleteInstanceRequest, InstanceRequest,
                                                          UserInstanceRegistry, ValidInstance)
from mcli.utils.utils_config import uuid_generator
from mcli.utils.utils_string_functions import (ensure_rfc1123_compatibility, snake_case_to_camel_case,
                                               validate_rfc1123_name)
from mcli.utils.utils_yaml import load_yaml

logger = logging.getLogger(__name__)
RUN_INPUT_UID_LENGTH = 4


@dataclass
class FinalRunConfig(DeserializableModel):
    """A finalized run configuration

    This configuration must be complete, with enough details to submit a new run to the
    MosaicML Cloud.
    """

    run_id: str
    name: str

    gpu_type: str
    gpu_num: int
    cpus: int

    platform: str
    image: str
    integrations: List[Dict[str, Any]]
    env_variables: List[Dict[str, str]]

    parameters: Dict[str, Any]

    # Make both optional for initial rollout
    # Eventually make entrypoint required and deprecate command
    command: str = ''
    entrypoint: str = ''

    _property_translations = {
        'run_id': 'run_id',
        'runName': 'name',
        'gpuType': 'gpu_type',
        'gpuNum': 'gpu_num',
        'cpus': 'cpus',
        'platform': 'platform',
        'image': 'image',
        'integrations': 'integrations',
        'envVariables': 'env_variables',
        'parameters': 'parameters',
        'command': 'command',
        'entrypoint': 'entrypoint',
    }

    def __str__(self) -> str:
        return yaml.safe_dump(asdict(self))

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> FinalRunConfig:
        missing = set(cls._property_translations) - set(response)
        if missing:
            raise MAPIException(
                status=HTTPStatus.BAD_REQUEST,
                message=
                f'Missing required key(s) in response to deserialize FinalRunConfig object: {", ".join(missing)}',
            )
        data = {v: response[k] for k, v in cls._property_translations.items()}
        return cls(**data)

    @classmethod
    def finalize_config(cls, run_config: RunConfig) -> FinalRunConfig:
        """Create a FinalRunConfig from the provided RunConfig.

        If the RunConfig is not fully populated then this function fails with an error.

        Args:
            run_config (RunConfig): The RunConfig

        Returns:
            FinalRunConfig: The FinalRunConfig object created using values from the RunConfig
        """

        if run_config.cpus is None:
            run_config.cpus = 0

        if run_config.platform:
            # Validate platform is valid
            _validate_platform_exists(run_config.platform)

        if not all((
                run_config.platform,
                run_config.gpu_type,
                run_config.gpu_num is not None,
        )):
            # Try to infer values from provided
            request = InstanceRequest(platform=run_config.platform,
                                      gpu_type=run_config.gpu_type,
                                      gpu_num=run_config.gpu_num)
            logger.debug(f'Incomplete instance request: {request}')
            user_instances = UserInstanceRegistry()
            options = user_instances.lookup(request)
            if len(options) == 1:
                valid_instance = options[0]
                logger.debug(f'Inferred a valid instance request: {valid_instance}')
                run_config.platform = valid_instance.platform
                run_config.gpu_type = valid_instance.gpu_type
                run_config.gpu_num = valid_instance.gpu_num
            else:
                valid_registry = ValidInstance.to_registry(options)
                raise IncompleteInstanceRequest(
                    requested=request,
                    options=valid_registry,
                    registry=user_instances.registry,
                )

        model_as_dict = asdict(run_config)

        # Remove deprecated run_name
        model_as_dict.pop('run_name', None)

        missing_fields = [field for field, value in model_as_dict.items() if value is None]
        if len(missing_fields) > 0:
            logger.error(f'[ERROR] Cannot construct run because of missing fields {missing_fields}.'
                         ' Please pass the missing fields either in a yaml file or as command line arguments.')
            missing_fields_string = ', '.join(missing_fields)
            raise Exception(f'Cannot construct FinalRunConfig with missing fields: {missing_fields_string}')

        # Fill in default initial values for FinalRunConfig
        model_as_dict.update({
            'run_id': uuid_generator(RUN_INPUT_UID_LENGTH),
        })

        if model_as_dict.get('name', None):
            run_name = model_as_dict['name']
            name_validation = validate_rfc1123_name(text=run_name)
            if not name_validation.valid:
                warning_prefix = 'WARNING: '
                logger.warning(warning_prefix + f'Invalid RFC 1123 Name: {run_name}')
                # TODO: Figure out why logging strips out regex []
                # (This is a rich formatting thing. [] is used to style text)
                logger.warning((warning_prefix + str(name_validation.message)))
                logger.warning(warning_prefix + 'Converting name to be RFC 1123 Compliant')
                new_run_name = ensure_rfc1123_compatibility(run_name)
                model_as_dict['name'] = new_run_name
                logger.warning(warning_prefix + f'New name: {new_run_name}')

        if isinstance(model_as_dict.get('gpu_type'), int):
            model_as_dict['gpu_type'] = str(model_as_dict['gpu_type'])

        # Do not support specifying both a command and an entrypoint because the two might
        # conflict with each other
        if run_config.command and run_config.entrypoint:
            raise Exception('Specifying both a command and entrypoint as input is not supported.'
                            'Please only specify one of command or entrypoint.')

        if not (run_config.command or run_config.entrypoint):
            raise Exception('Must specify one of command or entrypoint as input.')

        return cls(**model_as_dict)

    def to_create_run_api_input(self) -> Dict[str, Dict[str, Any]]:
        """Convert a run configuration to a proper JSON to pass to MAPI's createRun

        Returns:
            Dict[str, Dict[str, Any]]: The run configuration as a MAPI runInput JSON
        """
        translations = {v: k for k, v in self._property_translations.items()}

        translated_input = {}
        for field_name, value in asdict(self).items():
            translated_name = translations.get(field_name, field_name)
            translated_input[translated_name] = value

        # Convert integrations to the nested format MAPI expects
        if 'integrations' in translated_input:
            integrations_list = []
            for integration in translated_input['integrations']:
                integration_type = integration['integration_type']

                # Get all entries except integration_type so we can nest them under params
                del integration['integration_type']

                translated_integration = {}
                for param, val in integration.items():
                    # Translate keys to camel case for MAPI parameters
                    translated_key = snake_case_to_camel_case(param)
                    translated_integration[translated_key] = val

                integrations_dict = {'type': integration_type, 'params': translated_integration}
                integrations_list.append(integrations_dict)
            translated_input['integrations'] = integrations_list

        return {
            'runInput': translated_input,
        }


def _validate_platform_exists(platform: str):
    """Validate that the platform exists, if not throw a RuntimeError
    """
    try:
        _ = MCLIPlatform.get_by_name(platform)
    except KeyError as e:
        # pylint: disable-next=import-outside-toplevel
        from mcli.config import MCLIConfig

        conf = MCLIConfig.load_config(True)
        platform_names = ', '.join([pl.name for pl in conf.platforms])
        if platform_names:
            raise RuntimeError(f'Invalid platform requested: {platform}. '
                               'If you think this should be a valid platform, try creating the platform '
                               f'first with:\n\nmcli create platform {platform}\n\n'
                               f'Otherwise, choose one of: {platform_names}') from e
        else:
            raise RuntimeError(f'Invalid platform requested: {platform}. '
                               'User has not created any platforms. '
                               'If you think this should be a valid platform, try creating the platform '
                               f'first with:\n\nmcli create platform {platform}') from e


@dataclass
class RunConfig:
    """A run configuration for the MosaicML Cloud

    Values in here are not yet validated and some required values may be missing.

    Args:
        name (`Optional[str]`): User-defined name of the run
        gpu_type (`Optional[str]`): GPU type (optional if only one gpu type for your platform)
        gpu_num (`Optional[int]`): Number of GPUs
        cpus (`Optional[int]`): Number of CPUs
        platform (`Optional[str]`): Platform to use (optional if you only have one)
        image (`Optional[str]`): Docker image (e.g. `mosaicml/composer`)
        integrations (`List[Dict[str, Any]]`): List of integrations
        env_variables (`List[Dict[str, str]]`): List of environment variables
        command (`str`): Command to use when a run starts
        parameters (`Dict[str, Any]`): Parameters to mount into the environment
        entrypoint (`str`): Alternative to command
    """
    run_name: Optional[str] = None
    name: Optional[str] = None
    gpu_type: Optional[str] = None
    gpu_num: Optional[int] = None
    cpus: Optional[int] = None
    platform: Optional[str] = None
    image: Optional[str] = None
    integrations: List[Dict[str, Any]] = field(default_factory=list)
    env_variables: List[Dict[str, str]] = field(default_factory=list)

    command: str = ''
    parameters: Dict[str, Any] = field(default_factory=dict)
    entrypoint: str = ''

    def __post_init__(self):
        self.name = self.name or self.run_name
        if self.run_name is not None:
            logger.debug('Field "run_name" is deprecated. Please use "name" instead')

    def __str__(self) -> str:
        return yaml.safe_dump(asdict(self))

    @classmethod
    def empty(cls) -> RunConfig:
        return cls()

    @classmethod
    def from_file(cls, path: Union[str, Path]) -> RunConfig:
        """Load the config from the provided YAML file.

        Args:
            path (Union[str, Path]): Path to YAML file

        Returns:
            RunConfig: The RunConfig object specified in the YAML file
        """
        config = load_yaml(path)
        return cls.from_dict(config, show_unused_warning=True)

    @classmethod
    def from_dict(cls, dict_to_use: Dict[str, Any], show_unused_warning: bool = False) -> RunConfig:
        """Load the config from the provided dictionary.

        Args:
            dict_to_use (Dict[str, Any]): The dictionary to populate the RunConfig with

        Returns:
            RunConfig: The RunConfig object specified in the dictionary
        """
        field_names = list(map(lambda x: x.name, fields(cls)))

        unused_keys = []
        constructor = {}
        for key, value in dict_to_use.items():
            if key in field_names:
                constructor[key] = value

            else:
                unused_keys.append(key)

        if len(unused_keys) > 0 and show_unused_warning:
            warnings.warn(f'Encountered fields {unused_keys} which were not used in constructing the run.')

        return cls(**constructor)
