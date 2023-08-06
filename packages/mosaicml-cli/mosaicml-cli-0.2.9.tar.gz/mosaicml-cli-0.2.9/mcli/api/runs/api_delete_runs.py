""" Delete a run. """
from __future__ import annotations

from concurrent.futures import Future
from typing import List, Optional, Union, overload

from typing_extensions import Literal

from mcli.api.engine.engine import run_plural_mapi_request
from mcli.api.model.run import Run, get_run_schema
from mcli.api.schema.query import named_query
from mcli.api.types import GraphQLQueryVariable, GraphQLVariableType

__all__ = ['delete_runs']


@overload
def delete_runs(runs: Union[List[str], List[Run]],
                timeout: Optional[float] = 10,
                future: Literal[False] = False) -> List[Run]:
    ...


@overload
def delete_runs(runs: Union[List[str], List[Run]],
                timeout: Optional[float] = None,
                future: Literal[True] = True) -> Future[List[Run]]:
    ...


def delete_runs(runs: Union[List[str], List[Run]], timeout: Optional[float] = 10, future: bool = False):
    """Delete a list of runs in the MosaicML Cloud

    Any runs that are currently running will first be stopped.

    Args:
        runs: A list of runs or run names to delete
        timeout: Time, in seconds, in which the call should complete. If the call
            takes too long, a TimeoutError will be raised. If ``future`` is ``True``, this
            value will be ignored.
        future: Return the output as a :type concurrent.futures.Future:. If True, the
            call to `delete_run` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the :type Run: output, use ``return_value.result()``
            with an optional ``timeout`` argument.

    Returns:
        A list of :type Run: for the runs that were deleted
    """
    # Extract run names
    run_names = [r.name if isinstance(r, Run) else r for r in runs]

    filters = {}
    if run_names:
        filters['runName'] = {'in': run_names}

    query_function = 'deleteRun'
    get_variable_data_name = 'getRunsData'
    variables = {get_variable_data_name: {'filters': filters}}

    get_graphql_variable: GraphQLQueryVariable = GraphQLQueryVariable(
        variableName='getRunsData',
        variableDataName=get_variable_data_name,
        variableType=GraphQLVariableType.GET_RUNS_INPUT,
    )

    query = named_query(
        query_name='DeleteRun',
        query_function=query_function,
        query_items=get_run_schema(),
        variables=[get_graphql_variable],
        is_mutation=True,
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
