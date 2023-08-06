"""get_secrets SDK for MAPI"""
from __future__ import annotations

from concurrent.futures import Future
from typing import List, Optional, Union, overload

from typing_extensions import Literal

from mcli.api.engine.engine import run_plural_mapi_request
from mcli.api.engine.utils import dedent_indent
from mcli.api.schema.query import named_query
from mcli.api.types import GraphQLQueryVariable, GraphQLVariableType
from mcli.models.mcli_secret import MCLISecret, SecretType

__all__ = ['get_secrets']


def get_secret_schema(indentation: int = 2):
    """ Get the GraphQL schema for a :type SecretModel:
    Args:
        indentation (int): Optional[int] for the indentation of the block
    Returns:
        Returns a GraphQL string with all the fields needed to initialize a
        :type SecretModel:
    """
    return dedent_indent("""
name
type
metadata
value
        """, indentation)


@overload
def get_secrets(
    secrets: Optional[Union[List[str], List[MCLISecret]]] = None,
    secret_types: Optional[Union[List[str], List[SecretType]]] = None,
    timeout: Optional[float] = 10,
    future: Literal[False] = False,
) -> List[MCLISecret]:
    ...


@overload
def get_secrets(
    secrets: Optional[Union[List[str], List[MCLISecret]]] = None,
    secret_types: Optional[Union[List[str], List[SecretType]]] = None,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
) -> Future[List[MCLISecret]]:
    ...


def get_secrets(
    secrets: Optional[Union[List[str], List[MCLISecret]]] = None,
    secret_types: Optional[Union[List[str], List[SecretType]]] = None,
    timeout: Optional[float] = 10,
    future: bool = False,
):
    """Get all of the details stored about the requested secrets

    Arguments:
        secrets: List of secrets on which to get information
        secret_types: List of types to filter secrets on. This can be a list of str or
            :Type SecretType: objects. Only secrets of this type will be returned
        timeout: Time, in seconds, in which the call should complete. If the call
            takes too long, a TimeoutError will be raised. If ``future`` is ``True``, this
            value will be ignored.
        future: Return the output as a :type concurrent.futures.Future:. If True, the
            call to `get_secrets` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the list of secrets, use ``return_value.result()``
            with an optional ``timeout`` argument.

    Raises:
        MAPIException: If connecting to MAPI, raised when a MAPI communication error occurs
    """

    # Convert to strings
    secret_names = []
    if secrets:
        secret_names = [s.name if isinstance(s, MCLISecret) else s for s in secrets]

    filters = {}
    if secret_names:
        filters['name'] = {'in': secret_names}
    if secret_types:
        filters['type'] = {'in': secret_types}

    query_function = 'getSecrets'
    variable_data_name = 'getSecretsData'
    variables = {
        variable_data_name: {
            'filters': filters,
        },
    }

    graphql_variable: GraphQLQueryVariable = GraphQLQueryVariable(
        variableName='getSecretsData',
        variableDataName=variable_data_name,
        variableType=GraphQLVariableType.GET_SECRETS_INPUT,
    )

    query = named_query(
        query_name='GetSecrets',
        query_function=query_function,
        query_items=get_secret_schema(),
        variables=[graphql_variable],
        is_mutation=False,
    )

    response = run_plural_mapi_request(
        query=query,
        query_function=query_function,
        return_model_type=MCLISecret,
        variables=variables,
    )

    if not future:
        return response.result(timeout=timeout)
    else:
        return response
