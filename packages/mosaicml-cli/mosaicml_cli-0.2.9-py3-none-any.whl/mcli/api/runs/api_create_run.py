""" Create a Run """
from __future__ import annotations

from concurrent.futures import Future
from typing import Optional, Union, overload

from typing_extensions import Literal

from mcli.api.engine.engine import run_singular_mapi_request
from mcli.api.model.run import Run, get_run_schema
from mcli.api.schema.query import named_query
from mcli.api.types import GraphQLQueryVariable, GraphQLVariableType
from mcli.models.run_config import FinalRunConfig, RunConfig

__all__ = ['create_run']


@overload
def create_run(run: Union[RunConfig, FinalRunConfig],
               timeout: Optional[float] = 10,
               future: Literal[False] = False) -> Run:
    ...


@overload
def create_run(run: Union[RunConfig, FinalRunConfig],
               timeout: Optional[float] = None,
               future: Literal[True] = True) -> Future[Run]:
    ...


def create_run(run: Union[RunConfig, FinalRunConfig],
               timeout: Optional[float] = 10,
               future: bool = False) -> Union[Run, Future[Run]]:
    """Launch a run in the MosaicML Cloud

    The provided :class:`run <mcli.models.run_config.RunConfig>` must contain
    enough information to fully detail the run

    Args:
        run: A fully-configured run to launch. The run will be queued and persisted
            in the run database.
        timeout: Time, in seconds, in which the call should complete. If the run creation
            takes too long, a TimeoutError will be raised. If ``future`` is ``True``, this
            value will be ignored.
        future: Return the output as a :type concurrent.futures.Future:. If True, the
            call to `create_run` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the :type Run: output, use ``return_value.result()``
            with an optional ``timeout`` argument.

    Returns:
        A Run that includes the launched run details and the run status
    """

    if isinstance(run, RunConfig):
        run = FinalRunConfig.finalize_config(run)

    query_function = 'createRun'
    variable_data_name = 'createRunInput'
    variables = {
        variable_data_name: run.to_create_run_api_input(),
    }
    graphql_variable: GraphQLQueryVariable = GraphQLQueryVariable(
        variableName='createRunData',
        variableDataName=variable_data_name,
        variableType=GraphQLVariableType.CREATE_RUN_INPUT,
    )

    query = named_query(
        query_name='CreateRun',
        query_function=query_function,
        query_items=get_run_schema(),
        variables=[graphql_variable],
        is_mutation=True,
    )

    response = run_singular_mapi_request(
        query=query,
        query_function=query_function,
        return_model_type=Run,
        variables=variables,
    )

    if not future:
        return response.result(timeout=timeout)
    else:
        return response
