""" Functions for deleting MCLI objects """
import fnmatch
import logging
from typing import Dict, Generic, List, Optional, Tuple, TypeVar

from mcli.api.exceptions import KubernetesException, MAPIException
from mcli.api.kube.runs import delete_runs as kube_delete_runs
from mcli.api.kube.runs import get_runs as kube_get_runs
from mcli.api.runs import delete_runs, get_runs
from mcli.config import MESSAGE, FeatureFlag, MCLIConfig, MCLIConfigError
from mcli.models import MCLIPlatform
from mcli.objects.secrets.platform_secret import SecretManager
from mcli.utils.utils_interactive import query_yes_no
from mcli.utils.utils_logging import FAIL, INFO, OK, console, get_indented_list
from mcli.utils.utils_string_functions import is_glob

logger = logging.getLogger(__name__)

# pylint: disable-next=invalid-name
T_NOUN = TypeVar('T_NOUN')


class DeleteGroup(Generic[T_NOUN]):
    """Helper for extracting objects to delete from an existing set
    """

    def __init__(self, requested: List[str], existing: Dict[str, T_NOUN]):
        # Get unique values, with order
        self.requested = list(dict.fromkeys(requested))
        self.existing = existing

        self.chosen: Dict[str, T_NOUN] = {}
        self.missing: List[str] = []
        for pattern in self.requested:
            matching = fnmatch.filter(self.existing, pattern)
            if matching:
                self.chosen.update({k: self.existing[k] for k in matching})
            else:
                self.missing.append(pattern)

        self.remaining = {k: v for k, v in self.existing.items() if k not in self.chosen}


def delete_environment_variable(variable_names: List[str],
                                force: bool = False,
                                delete_all: bool = False,
                                **kwargs) -> int:
    del kwargs
    if not (variable_names or delete_all):
        logger.error(f'{FAIL} Must specify environment variable names or --all.')
        return 1
    try:
        conf = MCLIConfig.load_config()
    except MCLIConfigError:
        logger.error(MESSAGE.MCLI_NOT_INITIALIZED)
        return 1

    if delete_all:
        variable_names = ['*']

    group = DeleteGroup(variable_names, {ev.name: ev for ev in conf.environment_variables})

    # Some platforms couldn't be found. Throw a warning and continue
    if group.missing:
        logger.warning(f'{INFO} Could not find environment variable(s) matching: {", ".join(sorted(group.missing))}. '
                       f'Maybe you meant one of: {", ".join(sorted(list(group.remaining)))}?')

    # Nothing to delete, so error
    if not group.chosen:
        logger.error(f'{FAIL} No environment variables to delete')
        return 1

    if not force:
        if len(group.chosen) > 1:
            logger.info(f'{INFO} Ready to delete environment variables:\n'
                        f'{get_indented_list(sorted(list(group.chosen)))}\n')
            confirm = query_yes_no('Would you like to delete the environment variables listed above?')
        else:
            chosen_ev = list(group.chosen)[0]
            confirm = query_yes_no(f'Would you like to delete the environment variable: {chosen_ev}?')
        if not confirm:
            logger.error('Canceling deletion')
            return 1

    conf.environment_variables = list(group.remaining.values())
    conf.save_config()
    return 0


def delete_secret(secret_names: List[str], force: bool = False, delete_all: bool = False, **kwargs) -> int:
    """Delete the requested secret(s) from the user's platforms

    Args:
        secret_names: List of secrets to delete
        force: If True, do not request confirmation. Defaults to False.

    Returns:
        True if deletion was successful
    """
    del kwargs

    if not (secret_names or delete_all):
        logger.error(f'{FAIL} Must specify secret names or --all.')
        return 1

    try:
        conf = MCLIConfig.load_config()
    except MCLIConfigError:
        logger.error(MESSAGE.MCLI_NOT_INITIALIZED)
        return 1

    if not conf.platforms:
        logger.error(f'{FAIL} No platforms found. You must have at least 1 platform added before working with secrets.')
        return 1

    if delete_all:
        secret_names = ['*']

    # Note, we could just attempt to delete and catch the error.
    # I think it's a bit cleaner to first check if the secret exists, but this will be a bit slower
    # This slowness should be OK for secrets since they are generally small in number

    ref_platform = conf.platforms[0]
    secret_manager = SecretManager(ref_platform)

    group = DeleteGroup(secret_names, {ps.secret.name: ps for ps in secret_manager.get_secrets()})

    # Some platforms couldn't be found. Throw a warning and continue
    if group.missing:
        logger.warning(f'{INFO} Could not find secrets(s) matching: {", ".join(sorted(group.missing))}. '
                       f'Maybe you meant one of: {", ".join(sorted(list(group.remaining)))}?')

    if not group.chosen:
        logger.error(f'{FAIL} No secrets to delete')
        return 1

    if not force:
        if len(group.chosen) > 1:
            logger.info(f'{INFO} Ready to delete secrets:\n'
                        f'{get_indented_list(sorted(list(group.chosen)))}\n')
            confirm = query_yes_no('Would you like to delete the secrets listed above?')
        else:
            secret_name = list(group.chosen)[0]
            confirm = query_yes_no(f'Would you like to delete the secret: {secret_name}?')
        if not confirm:
            logger.error(f'{FAIL} Canceling deletion')
            return 1

    failures: Dict[str, List[str]] = {}
    with console.status('Deleting secrets...') as status:
        for platform in conf.platforms:
            with MCLIPlatform.use(platform):
                status.update(f'Deleting secrets from {platform.name}...')
                for ps in group.chosen.values():
                    success = ps.delete(platform.namespace)
                    if not success:
                        failures.setdefault(ps.secret.name, []).append(platform.name)

    deleted = sorted([name for name in group.chosen if name not in failures])
    if deleted:
        logger.info(f'{OK} Deleted secret(s): {", ".join(deleted)}')

    if failures:
        logger.error(f'{FAIL} Could not delete secret(s): {", ".join(sorted(list(failures.keys())))}')
        for name, failed_platforms in failures.items():
            logger.error(f'Secret {name} could not be deleted from platform(s): {", ".join(sorted(failed_platforms))}')
        return 1

    return 0


def delete_platform(platform_names: List[str], force: bool = False, delete_all: bool = False, **kwargs) -> int:
    del kwargs

    if not (platform_names or delete_all):
        logger.error(f'{FAIL} Must specify platform names or --all.')
        return 1

    try:
        conf = MCLIConfig.load_config()
    except MCLIConfigError:
        logger.error(MESSAGE.MCLI_NOT_INITIALIZED)
        return 1

    if delete_all:
        platform_names = ['*']

    group = DeleteGroup(platform_names, {pl.name: pl for pl in conf.platforms})

    # Some platforms couldn't be found. Throw a warning and continue
    if group.missing:
        logger.warning(f'{INFO} Could not find platform(s) matching: {", ".join(sorted(group.missing))}. '
                       f'Maybe you meant one of: {", ".join(sorted(list(group.remaining)))}?')

    # Nothing to delete, so error
    if not group.chosen:
        logger.error(f'{FAIL} No platforms to delete')
        return 1

    if not force:
        if len(group.chosen) > 1:
            logger.info(f'{INFO} Ready to delete platforms:\n'
                        f'{get_indented_list(sorted(list(group.chosen)))}\n')
            confirm = query_yes_no('Would you like to delete the platforms listed above?')
        else:
            chosen_platform = list(group.chosen)[0]
            confirm = query_yes_no(f'Would you like to delete the platform: {chosen_platform}?')
        if not confirm:
            logger.error(f'{FAIL} Canceling deletion')
            return 1

    conf.platforms = list(group.remaining.values())
    conf.save_config()

    logger.info(f"{OK} Deleted platform{'s' if len(group.chosen) > 1 else ''}: {', '.join(list(group.chosen.keys()))}")
    return 0


def _split_glob_filters(filters: List[str]) -> Tuple[List[str], Optional[List[str]]]:
    """Split a list of filters into glob-containing and non-glob-containing filters
    """

    globbers: List[str] = []
    non_globbers: Optional[List[str]] = []
    for f in filters:
        if is_glob(f):
            globbers.append(f)
        else:
            non_globbers.append(f)

    # Glob needs an all-match if all filters are non-glob
    if not globbers:
        globbers = ['*']

    # Non-glob filters needs to be None if all filters are glob
    if not non_globbers:
        non_globbers = None

    return globbers, non_globbers


def delete_run(name_filter: Optional[List[str]] = None,
               platform_filter: Optional[List[str]] = None,
               status_filter: Optional[List[str]] = None,
               delete_all: bool = False,
               force: bool = False,
               **kwargs):
    del kwargs

    if not (name_filter or platform_filter or status_filter or delete_all):
        logger.error(f'{FAIL} Must specify run names or at least one of --platform, --status, --all.')
        return 1

    if not name_filter:
        # Accept all that pass other filters
        name_filter = ['*']

    try:
        conf = MCLIConfig.load_config()
    except MCLIConfigError:
        logger.error(MESSAGE.MCLI_NOT_INITIALIZED)
        return 1

    if not conf.platforms:
        logger.error(f'{FAIL} No platforms found. You must have at least 1 platform added before working with runs.')
        return 1

    # Use get_runs only for the non-glob names provided. Any globs will be handled by DeleteGroup
    glob_filters, run_names = _split_glob_filters(name_filter)
    if conf.feature_enabled(FeatureFlag.USE_FEATUREDB):
        runs = get_runs(runs=run_names or None, platforms=platform_filter, statuses=status_filter)
    else:
        runs = kube_get_runs(runs=run_names or None, platforms=platform_filter, statuses=status_filter)
    group = DeleteGroup(glob_filters, {r.name: r for r in runs})

    # Some run name filters couldn't be found. Throw a warning and continue
    if group.missing:
        logger.warning(f'{INFO} Could not find run(s) matching: {", ".join(sorted(group.missing))}')

    if not group.chosen:
        logger.error(f'{FAIL} No runs found matching the specified criteria.')
        return 1

    if not force:
        if len(group.chosen) > 1:
            if len(group.chosen) >= 50:
                logger.info(f'Ready to delete {len(group.chosen)} runs')
                confirm = query_yes_no(f'Would you like to delete all {len(group.chosen)} runs?')
            else:
                logger.info(f'{INFO} Ready to delete runs:\n'
                            f'{get_indented_list(sorted(list(group.chosen)))}\n')
                confirm = query_yes_no('Would you like to delete the runs listed above?')
        else:
            chosen_run = list(group.chosen)[0]
            confirm = query_yes_no(f'Would you like to delete the run: {chosen_run}?')
        if not confirm:
            logger.error(f'{FAIL} Canceling deletion')
            return 1

    plural = 's' if len(group.chosen) > 1 else ''
    with console.status(f'Deleting run{plural}...') as console_status:
        runs = list(group.chosen.values())
        try:
            if conf.feature_enabled(FeatureFlag.USE_FEATUREDB):
                deleted = delete_runs(runs)
            else:
                deleted = kube_delete_runs(runs)
        except (KubernetesException, MAPIException, RuntimeError) as e:
            logger.error(f'{FAIL} {e}')
            return 1

        if not deleted:
            console_status.stop()
            logger.error('Run deletion failed in an unknown way')
            return 1

    logger.info(f'{OK} Deleted run{plural}')
    return 0
