""" Delete the DB """
from mcli.api.engine.engine import run_plural_mapi_request
from mcli.api.engine.utils import dedent_indent


def nuke_db() -> bool:
    """Runs a GraphQL query to wipe the DB

    Returns:
        Returns true if successful
    """

    query = dedent_indent("""
    mutation Mutation {
        nukeEverything
    }
    """)
    r = run_plural_mapi_request(query=query, query_function='nukeEverything')
    r.result(timeout=10)
    return True
