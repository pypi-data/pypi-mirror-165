""" GraphQL Query Helpers """
from typing import List, Optional

from mcli.api.engine.utils import dedent_indent
from mcli.api.types import GraphQLQueryVariable


def named_query(
    query_name: str,
    query_function: str,
    query_items: str,
    variables: Optional[List[GraphQLQueryVariable]] = None,
    is_mutation: bool = False,
) -> str:
    """Generates a Success Style Query for GraphQL

    Args:
        query_name: The name of the query (used for tracking purposes)
        query_function: The function that the GraphQL query should be calling
        query_item: An optional str for the fields needed to return a :type
            DeserializableModel:
        query_items: An str for the fields needed to return a list of
            :type DeserializableModel:
        variables: If the query takes variables, include them as a :type
            List[GraphQLQueryVariable]: to be passed to the function
        is_mutation: Set to False for queries and True for mutations

    Returns:
        The full GraphQL query string
    """
    selection_set = _get_selection_set(
        query_function=query_function,
        field_selection=_get_field_selection(query_items=query_items),
        variables=variables,
    )

    variables_string = ''
    if variables:
        _vars = [v.query_call_input for v in variables]
        variables_string = '(' + ', '.join(_vars) + ')'

    query_type = 'query' if not is_mutation else 'mutation'

    lines = [f'{query_type} {query_name}{variables_string} {{', selection_set, '}']
    return dedent_indent("\n".join(lines), 0)


def _get_selection_set(
    query_function: str,
    field_selection: str,
    variables: Optional[List[GraphQLQueryVariable]] = None,
    indentation: int = 2,
) -> str:
    variables_string = ''
    if variables:
        _vars = [v.selector_call_input for v in variables]
        variables_string = '(' + ', '.join(_vars) + ')'

    lines = [f'{query_function}{variables_string} {{', field_selection, '}']
    return dedent_indent("\n".join(lines), indentation)


def _get_field_selection(
    query_items: Optional[str] = None,
    indentation: int = 2,
) -> str:
    fields = ['status', 'message']
    if query_items:
        fields += ["items {", query_items, "}"]

    return dedent_indent("\n".join(fields), indentation)
