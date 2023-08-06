"""Implementation of mcli get runs"""
from __future__ import annotations

import argparse
import datetime as dt
import functools
import logging
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Generator, List, Optional

from mcli.api.exceptions import KubernetesException, MAPIException
from mcli.api.kube.runs import get_runs as kube_get_runs
from mcli.api.model.run import Run
from mcli.api.runs import get_runs
from mcli.cli.m_get.display import MCLIDisplayItem, MCLIGetDisplay, OutputDisplay
from mcli.config import MESSAGE, FeatureFlag, MCLIConfig, MCLIConfigError
from mcli.objects.platforms.platform_info import get_platform_list
from mcli.serverside.platforms import GPUType
from mcli.serverside.platforms.platform_instances import InstanceRequest, UserInstanceRegistry
from mcli.utils.utils_cli import comma_separated
from mcli.utils.utils_logging import FAIL, console
from mcli.utils.utils_run_status import CLI_STATUS_OPTIONS, cli_parse_run_status

logger = logging.getLogger(__name__)


def to_camel_case(text: str):
    return text.title().replace('_', '')


class RunColumns(Enum):
    NAME = 'name'
    PLATFORM = 'platform'
    GPU_TYPE = 'gpu_type'
    GPU_NUM = 'gpu_num'
    CREATED_TIME = 'created_time'
    START_TIME = 'start_time'
    END_TIME = 'end_time'
    STATUS = 'status'


def _format_timestamp(timestamp: Optional[dt.datetime], default='-') -> str:
    """Format timestamps for printing
    """

    if not timestamp:
        return default
    tz = dt.datetime.now(dt.timezone.utc).astimezone().tzinfo
    dt_format = '%Y-%m-%d %I:%M %p'
    return timestamp.astimezone(tz).strftime(dt_format)


@dataclass
class RunDisplayItem(MCLIDisplayItem):
    """Tuple that extracts run data for display purposes.
    """
    gpu_num: str
    created_time: str
    start_time: str
    end_time: str
    status: str
    platform: Optional[str] = None
    gpu_type: Optional[str] = None

    @classmethod
    def from_run(cls, run: Run, use_compact_view: bool) -> RunDisplayItem:
        extracted: Dict[str, str] = {RunColumns.NAME.value: run.name}
        if not use_compact_view:
            extracted[RunColumns.PLATFORM.value] = run.config.platform
            extracted[RunColumns.GPU_TYPE.value] = run.config.gpu_type
        extracted[RunColumns.GPU_NUM.value] = str(run.config.gpu_num)
        extracted[RunColumns.CREATED_TIME.value] = _format_timestamp(run.created_at)
        extracted[RunColumns.START_TIME.value] = _format_timestamp(run.started_at)
        extracted[RunColumns.END_TIME.value] = _format_timestamp(run.completed_at)
        extracted[RunColumns.STATUS.value] = to_camel_case(run.status.value)

        return RunDisplayItem(**extracted)


class MCLIRunDisplay(MCLIGetDisplay):
    """Display manager for runs
    """

    def __init__(self, models: List[Run]):
        self.models = sorted(models, key=lambda x: x.created_at, reverse=True)

        # Omit platform and gpu_type columns if there only exists one valid platform/gpu_type combination
        # available to the user
        self.use_compact_view = False
        platforms_list = get_platform_list()
        if len(platforms_list) == 1:
            request = InstanceRequest(platform=platforms_list[0].name, gpu_type=None, gpu_num=None)
            user_instances = UserInstanceRegistry()
            options = user_instances.lookup(request)
            num_gpu_types = len({x.gpu_type for x in options if GPUType.from_string(x.gpu_type) != GPUType.NONE})
            if num_gpu_types <= 1:
                self.use_compact_view = True

    @property
    def override_column_ordering(self) -> Optional[List[str]]:
        if self.use_compact_view:
            return [
                RunColumns.GPU_NUM.value, RunColumns.CREATED_TIME.value, RunColumns.START_TIME.value,
                RunColumns.END_TIME.value, RunColumns.STATUS.value
            ]
        return [e.value for e in RunColumns][1:]  # exclude 'name' column

    def __iter__(self) -> Generator[RunDisplayItem, None, None]:
        for model in self.models:
            item = RunDisplayItem.from_run(model, self.use_compact_view)
            yield item


def cli_get_runs(platform: Optional[List[str]] = None,
                 gpu_type: Optional[List[str]] = None,
                 gpu_num: Optional[List[int]] = None,
                 status: Optional[List[str]] = None,
                 output: OutputDisplay = OutputDisplay.TABLE,
                 **kwargs) -> int:
    """Get a table of ongoing and completed runs
    """
    del kwargs

    try:
        conf = MCLIConfig.load_config(safe=True)
        with console.status('Retrieving requested runs...'):
            if conf.feature_enabled(FeatureFlag.USE_FEATUREDB):
                runs = get_runs(platforms=platform, gpu_types=gpu_type, gpu_nums=gpu_num, statuses=status, timeout=None)
            else:
                runs = kube_get_runs(platforms=platform,
                                     gpu_types=gpu_type,
                                     gpu_nums=gpu_num,
                                     statuses=status,
                                     timeout=None)
        display = MCLIRunDisplay(runs)
        display.print(output)
    except (KubernetesException, MAPIException) as e:
        logger.error(f'{FAIL} {e}')
        return 1
    except RuntimeError as e:
        logger.error(f'{FAIL} {e}')
        return 1
    except MCLIConfigError:
        logger.error(MESSAGE.MCLI_NOT_INITIALIZED)
        return 1

    return 0


def get_runs_argparser(subparsers: argparse._SubParsersAction):
    """Configures the ``mcli get runs`` argparser
    """

    run_examples: str = """Examples:
    $ mcli get runs

    NAME                         PLATFORM   GPU_TYPE      GPU_NUM      CREATED_TIME     STATUS
    run-foo                      p-1        g0-type       8            05/06/22 1:58pm  Completed
    run-bar                      p-2        g0-type       1            05/06/22 1:57pm  Completed
    """
    runs_parser = subparsers.add_parser('runs',
                                        aliases=['run'],
                                        help='Get information on all of your existing runs across all platforms.',
                                        epilog=run_examples,
                                        formatter_class=argparse.RawDescriptionHelpFormatter)
    runs_parser.add_argument(
        '-p',
        '--platform',
        metavar='PLATFORM',
        default=None,
        type=comma_separated,
        help='Filter to just runs on specific platforms. '
        'Multiple platforms should be specified using a comma-separated list, e.g. "platform1,platform2"')

    runs_parser.add_argument(
        '-t',
        '--gpu-type',
        metavar='GPU',
        default=None,
        type=comma_separated,
        help='Filter to just runs on specific GPU type. '
        'Multiple gpus should be specified using a comma-separated list, e.g. "a100_40gb,v100_16gb"')
    runs_parser.add_argument('-n',
                             '--gpu-num',
                             metavar='# GPUs',
                             default=None,
                             type=functools.partial(comma_separated, fun=int),
                             help='Filter to just runs of a specific number of GPUs. '
                             'Multiple values should be specified using a comma-separated list, e.g. "1,8"')

    runs_parser.add_argument(
        '-s',
        '--status',
        default=None,
        metavar='STATUS',
        type=functools.partial(comma_separated, fun=cli_parse_run_status),
        help=f'Filter to just runs with the specified statuses (choices: {", ".join(CLI_STATUS_OPTIONS)}). '
        'Multiple statuses should be specified using a comma-separated list, e.g. "failed,completed"')
    runs_parser.set_defaults(func=cli_get_runs)

    return runs_parser
