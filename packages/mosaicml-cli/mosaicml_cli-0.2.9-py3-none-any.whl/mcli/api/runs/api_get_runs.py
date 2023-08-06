"""get_runs SDK for MAPI"""
from __future__ import annotations

from concurrent.futures import Future
from typing import List, Optional, Union, overload

from typing_extensions import Literal

from mcli.api.engine.engine import run_plural_mapi_request
from mcli.api.model.run import Run, get_run_schema
from mcli.api.schema.query import named_query
from mcli.api.types import GraphQLQueryVariable, GraphQLVariableType
from mcli.models.mcli_platform import MCLIPlatform
from mcli.serverside.platforms.gpu_type import GPUType
from mcli.utils.utils_run_status import RunStatus

__all__ = ['get_runs']


@overload
def get_runs(
    runs: Optional[Union[List[str], List[Run]]] = None,
    platforms: Optional[Union[List[str], List[MCLIPlatform]]] = None,
    gpu_types: Optional[Union[List[str], List[GPUType]]] = None,
    gpu_nums: Optional[List[int]] = None,
    statuses: Optional[Union[List[str], List[RunStatus]]] = None,
    timeout: Optional[float] = 10,
    future: Literal[False] = False,
) -> List[Run]:
    ...


@overload
def get_runs(
    runs: Optional[Union[List[str], List[Run]]] = None,
    platforms: Optional[Union[List[str], List[MCLIPlatform]]] = None,
    gpu_types: Optional[Union[List[str], List[GPUType]]] = None,
    gpu_nums: Optional[List[int]] = None,
    statuses: Optional[Union[List[str], List[RunStatus]]] = None,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
) -> Future[List[Run]]:
    ...


def get_runs(
    runs: Optional[Union[List[str], List[Run]]] = None,
    platforms: Optional[Union[List[str], List[MCLIPlatform]]] = None,
    gpu_types: Optional[Union[List[str], List[GPUType]]] = None,
    gpu_nums: Optional[List[int]] = None,
    statuses: Optional[Union[List[str], List[RunStatus]]] = None,
    timeout: Optional[float] = 10,
    future: bool = False,
):
    """List runs that have been launched in the MosaicML Cloud

    The returned list will contain all of the details stored about the requested runs.

    Arguments:
        runs: List of runs on which to get information
        platforms: List of platforms to filter runs. This can be a list of str or
            :type MCLIPlatform: objects. Only runs submitted to these platforms will be
            returned.
        gpu_types: List of gpu types to filter runs. This can be a list of str or
            :type GPUType: enums. Only runs scheduled on these GPUs will be returned.
        gpu_nums: List of gpu counts to filter runs. Only runs scheduled on this number
            of GPUs will be returned.
        statuses: List of run statuses to filter runs. This can be a list of str or
            :type RunStatus: enums. Only runs currently in these phases will be returned.
        timeout: Time, in seconds, in which the call should complete. If the call
            takes too long, a TimeoutError will be raised. If ``future`` is ``True``, this
            value will be ignored.
        future: Return the output as a :type concurrent.futures.Future:. If True, the
            call to `get_runs` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the list of runs, use ``return_value.result()``
            with an optional ``timeout`` argument.

    Raises:
        MAPIException: If connecting to MAPI, raised when a MAPI communication error occurs
    """

    # Convert to strings
    run_names = []
    if runs:
        run_names = [r.name if isinstance(r, Run) else r for r in runs]

    filters = {}
    if run_names:
        filters['runName'] = {'in': run_names}
    if statuses:
        filters['runStatus'] = {'in': statuses}
    if platforms:
        filters['platform'] = {'in': platforms}
    if gpu_types:
        filters['gpuType'] = {'in': gpu_types}
    if gpu_nums:
        filters['gpuNum'] = {'in': gpu_nums}

    query_function = 'getRuns'
    variable_data_name = 'getRunsData'
    variables = {
        variable_data_name: {
            'filters': filters,
            'includeDeleted': False,
        },
    }

    graphql_variable: GraphQLQueryVariable = GraphQLQueryVariable(
        variableName='getRunsData',
        variableDataName=variable_data_name,
        variableType=GraphQLVariableType.GET_RUNS_INPUT,
    )

    query = named_query(
        query_name='GetRuns',
        query_function=query_function,
        query_items=get_run_schema(),
        variables=[graphql_variable],
        is_mutation=False,
    )

    response = run_plural_mapi_request(
        query=query,
        query_function=query_function,
        return_model_type=Run,
        variables=variables,
    )

    if not future:
        return response.result(timeout=timeout)
    else:
        return response
