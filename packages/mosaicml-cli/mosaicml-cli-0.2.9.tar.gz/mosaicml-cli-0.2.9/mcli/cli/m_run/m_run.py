""" mcli run Entrypoint """
import argparse
import logging
import textwrap
from typing import Optional

from rich.ansi import AnsiDecoder

from mcli.api.exceptions import KubernetesException, MAPIException
from mcli.api.runs import create_run
from mcli.config import FeatureFlag, MCLIConfig
from mcli.models.mcli_platform import MCLIPlatform
from mcli.sdk import Run, RunConfig
from mcli.sdk import create_run as kube_create_run
from mcli.sdk import delete_runs, follow_run_logs, wait_for_run_status
from mcli.serverside.platforms.platform import InvalidPriorityError, PriorityLabel
from mcli.serverside.platforms.platform_instances import (IncompleteInstanceRequest, InstanceTypeUnavailable,
                                                          UserInstanceRegistry)
from mcli.utils.utils_epilog import CommonLog, EpilogSpinner, RunEpilog
from mcli.utils.utils_logging import FAIL, INFO, OK, console
from mcli.utils.utils_run_status import PodStatus, RunStatus

logger = logging.getLogger(__name__)


def print_help(**kwargs) -> int:
    del kwargs
    mock_parser = argparse.ArgumentParser()
    _configure_parser(mock_parser)
    mock_parser.print_help()
    return 1


def follow_run(run: Run) -> int:
    final_config = run.config
    with MCLIPlatform.use(final_config.platform) as platform:
        logger.info(f'{INFO} Run [cyan]{run.name}[/] submitted. Waiting for it to start...')
        logger.info(f'{INFO} You can press Ctrl+C to quit and follow your run manually.')
        epilog = RunEpilog(run.name, platform.namespace)
        last_status: Optional[PodStatus] = None
        with EpilogSpinner() as spinner:
            last_status = epilog.wait_until(callback=spinner, timeout=300)

        # Wait timed out
        common_log = CommonLog(logger)
        if last_status is None:
            common_log.log_timeout()
            return 0
        elif last_status.state == RunStatus.FAILED_PULL:
            common_log.log_pod_failed_pull(run.name, final_config.image)
            with console.status('Deleting failed run...'):
                delete_runs([run])
            return 1
        elif last_status.state == RunStatus.FAILED:
            common_log.log_pod_failed(run.name)
            return 1
        elif last_status.state.before(RunStatus.RUNNING):
            common_log.log_unknown_did_not_start()
            logger.debug(last_status)
            return 1

        logger.info(f'{OK} Run [cyan]{run.name}[/] started')
        logger.info(f'{INFO} Following run logs. Press Ctrl+C to quit.\n')
        decoder = AnsiDecoder()
        for line in follow_run_logs(run, rank=0):
            console.print(decoder.decode_line(line))

        wait_for_run_status(run, status=RunStatus.COMPLETED, timeout=10)

    return 0


def run_entrypoint(
    file: str,
    priority: Optional[PriorityLabel] = None,
    follow: bool = True,
    override_platform: Optional[str] = None,
    override_gpu_type: Optional[str] = None,
    override_gpu_num: Optional[int] = None,
    override_image: Optional[str] = None,
    override_name: Optional[str] = None,
    **kwargs,
) -> int:
    del kwargs

    if file is None:
        return print_help()

    logger.info(
        textwrap.dedent("""
    ------------------------------------------------------
    Let's run this run
    ------------------------------------------------------
    """))

    platform_name: Optional[str] = None
    try:
        run_config = RunConfig.from_file(path=file)

        # command line overrides
        # only supports basic format for now and not structured params
        if override_platform is not None:
            run_config.platform = override_platform

        if override_gpu_type is not None:
            run_config.gpu_type = override_gpu_type

        if override_gpu_num is not None:
            run_config.gpu_num = override_gpu_num

        if override_image is not None:
            run_config.image = override_image

        if override_name is not None:
            run_config.name = override_name

        conf = MCLIConfig.load_config(safe=True)
        with console.status('Submitting run...'):
            if conf.feature_enabled(FeatureFlag.USE_FEATUREDB):
                run = create_run(run=run_config, timeout=None)
            else:
                run = kube_create_run(run=run_config, _priority=priority, timeout=None)
        platform_name = run.config.platform

        if not follow:
            message = f"""
            {OK} Run [cyan]{run.name}[/] submitted.

            To see the run\'s status, use:

            [bold]mcli get runs[/]

            To see the run\'s logs, use:

            [bold]mcli logs {run.name}[/]
            """
            logger.info(textwrap.dedent(message).strip())
            return 0
        else:
            return follow_run(run)

    except (MAPIException, KubernetesException) as e:
        logger.error(f'{FAIL} {e}')
        return 1
    except (IncompleteInstanceRequest, InstanceTypeUnavailable) as e:
        logger.error(e)
        return 1
    except InvalidPriorityError as e:
        e.platform = platform_name
        logger.error(f'{FAIL} {e}')
        return 1
    except RuntimeError as e:
        logger.error(f'{FAIL} {e}')
        return 1
    except (NotADirectoryError, FileNotFoundError) as e:
        logger.error(f'{FAIL} {e}')
        return 1


def add_run_argparser(subparser: argparse._SubParsersAction) -> None:
    run_parser: argparse.ArgumentParser = subparser.add_parser(
        'run',
        aliases=['r'],
        help='Run stuff',
    )
    run_parser.set_defaults(func=run_entrypoint)
    _configure_parser(run_parser)


def _configure_parser(parser: argparse.ArgumentParser):
    parser.add_argument(
        '-f',
        '--file',
        dest='file',
        help='File from which to load arguments.',
    )

    parser.add_argument(
        '--priority',
        choices=list(PriorityLabel),
        type=PriorityLabel.ensure_enum,
        help='Priority level at which runs should be submitted. '
        '(default None)',
    )

    parser.add_argument(
        '--no-follow',
        action='store_false',
        dest='follow',
        default=False,
        help='Do not automatically try to follow the run\'s logs. This is the default behavior',
    )

    parser.add_argument('--follow',
                        action='store_true',
                        dest='follow',
                        default=False,
                        help='Follow the logs of an in-progress run.')

    user_registry = UserInstanceRegistry()
    available_platforms = sorted(list(user_registry.registry.keys()))

    parser.add_argument(
        '--platform',
        dest='override_platform',
        choices=available_platforms,
        help='Optional override for MCLI platform',
    )

    available_types, available_nums = set(), set()
    for instance in user_registry.registry.values():
        for gpu_type, gpu_nums in instance.items():
            if gpu_type.value != 'none':
                available_types.add(str(gpu_type))
            available_nums.update(set(gpu_nums))
    gpu_types = sorted(list(available_types))
    gpu_nums = sorted(list(available_nums))

    parser.add_argument(
        '--gpu-type',
        dest='override_gpu_type',
        choices=gpu_types,
        help='Optional override for GPU type. Valid GPU type depend on'
        ' the platform and GPU number requested',
    )

    parser.add_argument(
        '--gpus',
        type=int,
        dest='override_gpu_num',
        choices=gpu_nums,
        help='Optional override for number of GPUs. Valid GPU numbers '
        'depend on the platform and GPU type',
    )

    parser.add_argument(
        '--image',
        dest='override_image',
        help='Optional override for docker image',
    )

    parser.add_argument(
        '--name',
        '--run-name',
        dest='override_name',
        help='Optional override for run name',
    )
