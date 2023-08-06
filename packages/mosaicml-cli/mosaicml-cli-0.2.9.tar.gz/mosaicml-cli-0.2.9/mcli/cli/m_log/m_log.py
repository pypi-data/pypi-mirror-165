"""mcli logs entrypoint"""
import argparse
import logging
import os
import sys
from http import HTTPStatus
from typing import Optional

from kubernetes.client.exceptions import ApiException
from rich.ansi import AnsiDecoder

from mcli.api.exceptions import KubernetesException, MAPIException
from mcli.api.kube.runs import delete_runs, follow_run_logs, get_run_logs, get_runs
from mcli.api.model.run import Run
from mcli.config import MESSAGE, FeatureFlag, MCLIConfig, MCLIConfigError
from mcli.models.mcli_platform import MCLIPlatform
from mcli.utils.utils_epilog import CommonLog, EpilogSpinner, RunEpilog
from mcli.utils.utils_logging import FAIL, INFO, console, err_console
from mcli.utils.utils_run_status import PodStatus, RunStatus

logger = logging.getLogger(__name__)


def get_latest_run() -> Run:
    """Retrieve the latest run for the user
    """
    runs = get_runs(future=False)
    if not runs:
        raise KubernetesException(status=HTTPStatus.NOT_FOUND, message='No runs found')
    return sorted(runs, key=lambda x: x.created_at, reverse=True)[0]


# pylint: disable-next=too-many-statements
def get_logs(
    run_name: Optional[str] = None,
    rank: Optional[int] = None,
    follow: bool = False,
    **kwargs,
) -> int:
    del kwargs

    try:
        conf = MCLIConfig.load_config()
        if conf.feature_enabled(FeatureFlag.USE_FEATUREDB):
            logger.error(f'{FAIL} {NotImplementedError("MAPI does not yet support retrieval of run logs")}')
            return 1

        run: Optional[Run] = None
        with err_console.status('Getting run details...') as spinner:
            if run_name is None:
                spinner.update('No run name provided. Finding latest run...')
                run = get_latest_run()
                logger.info(f'{INFO} No run name provided. Displaying log for [blue]{run.name}[/]')
            else:
                runs = get_runs([run_name])
                if not runs:
                    raise KubernetesException(status=HTTPStatus.NOT_FOUND, message=f'Could not find run: {run_name}')
                run = runs[0]

        if follow and run.status.after(RunStatus.QUEUED) and run.status.before(RunStatus.RUNNING):
            timeout = 300
            with MCLIPlatform.use(run.config.platform) as platform:
                # Pod is creating, so let's use an epilog
                logger.info(f'{INFO} Waiting for run to start, press Ctrl+C to quit')
                epilog = RunEpilog(run.name, platform.namespace)
                status: Optional[PodStatus] = None
                with EpilogSpinner() as spinner:
                    status = epilog.wait_until(callback=spinner, timeout=timeout)
                if status is None:
                    # Pod epilog timed out
                    logger.info(f'{INFO} Run {run.name} did not start within {timeout} seconds. Try again later.')
                    return 1
                run.status = status.state
        if run.status == RunStatus.FAILED_PULL:
            CommonLog(logger).log_pod_failed_pull(run.name, run.config.image)
            with console.status('Deleting failed run...'):
                delete_runs([run])
            return 1
        elif run.status.before(RunStatus.QUEUED, inclusive=True):
            # Pod still waiting to be scheduled. Return
            logger.error(f'{FAIL} Run {run.name} has not been scheduled')
            return 1
        elif run.status.before(RunStatus.RUNNING):
            # Pod still not running, probably because follow==False
            logger.error(f'{FAIL} Run has not yet started. You can check the status with `mcli get runs` '
                         'and try again later.')
            return 1
        decoder = AnsiDecoder()
        if follow:
            for line in follow_run_logs(run, rank=rank):
                console.print(decoder.decode_line(line))
        else:
            for line in get_run_logs(run, rank=rank).splitlines():
                console.print(decoder.decode_line(line))

    except (KubernetesException, MAPIException) as e:
        logger.error(f'{FAIL} {e}')
        return 1
    except ApiException as e:
        e = KubernetesException.transform_api_exception(e)
        logger.error(f'{FAIL} {e}')
        return 1
    except RuntimeError as e:
        logger.error(f'{FAIL} {e}')
        return 1
    except MCLIConfigError:
        logger.error(MESSAGE.MCLI_NOT_INITIALIZED)
        return 1
    except BrokenPipeError:
        # This is raised when output is piped to programs like `head`
        # Error handling taken from this example in the python docs:
        # https://docs.python.org/3/library/signal.html#note-on-sigpipe
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())

        return 1

    return 0


def configure_argparser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.set_defaults(func=get_logs)
    parser.add_argument('run_name',
                        metavar='RUN',
                        nargs='?',
                        help='The name of the run. If not provided, will return the logs of the latest run')
    parser.add_argument('--rank',
                        type=int,
                        default=None,
                        metavar='N',
                        help='Rank of the node in a multi-node run whose logs you\'d like to view')
    follow_grp = parser.add_mutually_exclusive_group()
    follow_grp.add_argument('--no-follow',
                            action='store_false',
                            dest='follow',
                            default=False,
                            help='Do not follow the logs of an in-progress run. '
                            'Simply print any existing logs and exit. This is the default behavior.')
    follow_grp.add_argument('-f',
                            '--follow',
                            action='store_true',
                            dest='follow',
                            default=False,
                            help='Follow the logs of an in-progress run.')

    return parser


def add_log_parser(subparser: argparse._SubParsersAction):
    """Add the parser for retrieving run logs
    """

    # pylint: disable=invalid-name
    EXAMPLES = """

Examples:

# View the current logs of an ongoing run
> mcli logs run-1234

# By default, if you don't specify the run name the logs for the latest run will be retrieved
> mcli logs

# View the logs of a specific node in a multi-node run
> mcli logs multinode-run-1234 --rank 1

# Follow the logs for an ongoing run
> mcli logs run-1234 --follow
"""

    log_parser: argparse.ArgumentParser = subparser.add_parser(
        'logs',
        aliases=['log'],
        help='View the logs from a specific run',
        description='View the logs of an ongoing, completed or failed run',
        epilog=EXAMPLES,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    log_parser = configure_argparser(log_parser)

    return log_parser
