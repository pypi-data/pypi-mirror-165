""" MCLI Abstraction for Secrets """
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from http import HTTPStatus
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Type

import yaml

from mcli.api.exceptions import MAPIException
from mcli.api.schema.generic_model import DeserializableModel
from mcli.models import MCLIPlatform
from mcli.serverside.job.mcli_k8s_job import MCLIK8sJob
from mcli.utils.utils_kube import base64_decode, base64_encode, read_secret
from mcli.utils.utils_kube_labels import label
from mcli.utils.utils_serializable_dataclass import SerializableDataclass, T_SerializableDataclass
from mcli.utils.utils_types import CommonEnum

SECRET_MOUNT_PATH_PARENT = Path('/secrets')


class SecretType(CommonEnum):
    """ Enum for Types of Secrets Allowed """

    docker_registry = 'docker_registry'
    environment = 'environment'
    generic = 'generic'
    git = 'git'
    mounted = 'mounted'
    s3_credentials = 's3_credentials'
    sftp = 'sftp'
    ssh = 'ssh'
    s3 = 's3'


DEPRECATED_SECRETS: Dict[SecretType, SecretType] = {SecretType.s3_credentials: SecretType.s3}


def secret_type_to_class(secret_type: SecretType) -> Type[MCLISecret]:
    """Maps the secret type to MCLISecret subclass"""

    # pylint: disable-next=import-outside-toplevel
    from mcli.objects.secrets import (MCLIDockerRegistrySecret, MCLIEnvVarSecret, MCLIGitSSHSecret, MCLIMountedSecret,
                                      MCLIS3Secret, MCLISSHSecret)

    secret_type_to_class_dict = {
        SecretType.docker_registry: MCLIDockerRegistrySecret,
        SecretType.mounted: MCLIMountedSecret,
        SecretType.environment: MCLIEnvVarSecret,
        SecretType.ssh: MCLISSHSecret,
        SecretType.git: MCLIGitSSHSecret,
        SecretType.s3_credentials: MCLIS3Secret,
        SecretType.s3: MCLIS3Secret
    }

    if secret_type in secret_type_to_class_dict:
        return secret_type_to_class_dict[secret_type]
    else:
        raise NotImplementedError(f'Secret of type: { secret_type } not supported yet')


@dataclass
class MCLISecret(SerializableDataclass, DeserializableModel, ABC):
    """
    The Base Secret Class for MCLI Secrets

    Secrets can not nest other SerializableDataclass objects
    """

    name: str
    secret_type: SecretType

    @property
    def kubernetes_type(self) -> str:
        """The corresponding Kubernetes secret type for this class of secrets
        """
        return 'Opaque'

    @abstractmethod
    def add_to_job(self, kubernetes_job: MCLIK8sJob) -> bool:
        """Add a secret to a job
        """

    @property
    def required_packing_fields(self) -> Set[str]:
        """ All required fields for packing up the secret """
        return set()

    def unpack(self, data: Dict[str, str]):
        """Unpack the Kubernetes secret `data` field to fill in required secret values

        All required packing fields must be present.
        By default looks for all required fields and base64 decodes them

        Args:
            data (Dict[str, str]): Kubernetes `data` field as a JSON
        """

        missing_fields = self.required_packing_fields - data.keys()
        if missing_fields:
            raise ValueError('Missing required field(s) to unpack Secret: '
                             f'{",".join(missing_fields)}')

        for field_ in self.required_packing_fields:
            setattr(self, field_, base64_decode(data[field_]))

    def pack(self) -> Dict[str, str]:
        """The `data` field for the corresponding kubernetes secret
        Validated to ensure fully completed

        By default base64 encodes all required fields
        """
        filled_fields = asdict(self)
        data = {k: v for k, v in filled_fields.items() if k in self.required_packing_fields}
        for key, value in data.items():
            if not isinstance(value, str):
                raise TypeError(f'All keys in a secret must be strings, got {key}: {type(value)}')
            data[key] = base64_encode(value)
        return data

    def pull(self, platform: MCLIPlatform):
        with MCLIPlatform.use(platform):
            # Read the secret if it exists
            secret = read_secret(self.name, platform.namespace)
            if not secret:
                raise RuntimeError(f'Could not find secret {self.name} in platform {platform.name}')
            assert isinstance(secret['data'], dict)
            self.unpack(secret['data'])

    @classmethod
    def from_dict(cls: Type[T_SerializableDataclass], data: Dict[str, Any]) -> T_SerializableDataclass:
        if not isinstance(data, dict):
            raise TypeError(f'Secret data must be structured as a dictionary. Got: {type(data)}')

        secret_type = data.get('secret_type', None)
        if not secret_type:
            raise ValueError(f'No `secret_type` found for secret with data: \n{yaml.dump(data)}')

        secret_type: SecretType = SecretType.ensure_enum(secret_type)
        data['secret_type'] = secret_type

        secret: Optional[MCLISecret] = None
        secret_type = DEPRECATED_SECRETS.get(secret_type, secret_type)
        secret_type_cls = secret_type_to_class(secret_type)
        secret = secret_type_cls(**data)
        assert isinstance(secret, MCLISecret)
        return secret  # type: ignore

    @property
    def kubernetes_labels(self) -> Dict[str, str]:
        """Labels to add to all Kubernetes secrets
        """
        labels = {
            label.mosaic.SECRET_TYPE: self.secret_type.value.replace('_', '-'),
            **label.mosaic.version.get_version_labels(),
        }
        return labels

    @property
    def kubernetes_annotations(self) -> Dict[str, str]:
        """Annotations to add to all Kubernetes secrets
        """
        return {}

    @staticmethod
    def _mapi_required_properties() -> Tuple[str]:
        """Required properties for mapi response"""
        return tuple(['name', 'type', 'metadata', 'value'])

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> MCLISecret:
        required_properties = set(cls._mapi_required_properties())
        missing = required_properties - set(response)
        if missing:
            raise MAPIException(
                status=HTTPStatus.BAD_REQUEST,
                message=f'Missing required key(s) in response to deserialize Secret object: {", ".join(missing)}',
            )

        try:
            secret_type = SecretType[response['type'].lower()]
            secret_type = DEPRECATED_SECRETS.get(secret_type, secret_type)
            secret_type_cls = secret_type_to_class(secret_type)

            secret = secret_type_cls(name=response['name'], secret_type=response['type'].lower())

            if secret_type in {SecretType.mounted, SecretType.ssh, SecretType.git}:
                setattr(secret, 'mount_path', response['metadata']['mountPath'])
            elif secret_type == SecretType.environment:
                setattr(secret, 'key', response['metadata']['key'])
            elif secret_type in {SecretType.s3_credentials, SecretType.s3}:
                setattr(secret, 'mount_directory', response['metadata']['mountDirectory'])
                setattr(secret, 'credentials', response['value']['credentials'])
                setattr(secret, 'config', response['value']['config'])

            return secret
        except KeyError as exc:
            raise MAPIException(
                status=HTTPStatus.BAD_REQUEST,
                message=f'Secret type {response["type"]} not supported yet.',
            ) from exc


@dataclass
class MCLIGenericSecret(MCLISecret):
    """Secret class for generic secrets
    """
    value: Optional[str] = None

    @property
    def disk_skipped_fields(self) -> List[str]:
        return ['value']

    @property
    def required_packing_fields(self) -> Set[str]:
        return set(self.disk_skipped_fields)

    def add_to_job(self, kubernetes_job: MCLIK8sJob) -> bool:
        del kubernetes_job
        # Missing context on how it should be added to a job
        raise NotImplementedError
