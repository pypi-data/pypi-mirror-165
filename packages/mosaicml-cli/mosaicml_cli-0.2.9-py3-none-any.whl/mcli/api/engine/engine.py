""" GraphQL Query Engine """
from __future__ import annotations

import json
import logging
from concurrent.futures import Future, ThreadPoolExecutor
from http import HTTPStatus
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, cast

import requests

from mcli.api.exceptions import KubernetesException, MAPIException, MCLIConfigError, MultiMAPIException
from mcli.api.schema.generic_model import DeserializableModel
from mcli.api.schema.query_models import RawSuccessResponse, SuccessResponse
from mcli.config import Messages

logger = logging.getLogger(__name__)

# pylint: disable-next=invalid-name
THREADPOOL_WORKERS = 10
THREADPOOL: Optional[ThreadPoolExecutor] = None


def _create_threadpool() -> ThreadPoolExecutor:
    """Create a global threadpool for requests
    """
    global THREADPOOL
    THREADPOOL = ThreadPoolExecutor(max_workers=THREADPOOL_WORKERS, thread_name_prefix='mosaicml-api')
    return THREADPOOL


class MAPIConnection:
    """Connection to a user's MAPI instance

    Args:
        api_key: The user's API key. If not specified, the value of the $MOSAICML_API_KEY
            environment variable will be used. If that does not exist, the value in the
            user's config file will be used. If that does not exist, a MAPIException will
            be thrown.
        endpoint: The MAPI URL to hit for all requests. If not specified, the value of the
            $MOSAICML_API_ENDPOINT environment variable will be used. If that does not
            exist, the default setting will be used.
        pool: An optional threadpool to use for all connection requests. If not provided,
            a shared pool will be used for all requests.

    Raises:
        MAPIException: Raised if the user does not have an API key set
    """
    api_key: str
    endpoint: str

    def __init__(self,
                 api_key: Optional[str] = None,
                 endpoint: Optional[str] = None,
                 pool: Optional[ThreadPoolExecutor] = None):
        self._load_from_environment(api_key, endpoint)
        self._pool = pool
        self._prev: Optional[MAPIConnection] = None

    def _load_from_environment(self, api_key: Optional[str] = None, endpoint: Optional[str] = None) -> None:
        # pylint: disable-next=import-outside-toplevel
        from mcli import config

        if api_key is None:
            api_key = config.MCLIConfig().load_config().MOSAICML_API_KEY

        if api_key is None:
            raise MCLIConfigError(Messages.MCLI_NOT_INITIALIZED)
        self.api_key = api_key

        if endpoint is None:
            config.env_str_override_config('MOSAICML_API_ENDPOINT')
            endpoint = config.MOSAICML_API_ENDPOINT
        self.endpoint = endpoint

    @staticmethod
    def _set_connection(connection: Optional[MAPIConnection]) -> None:
        """Set the current connection instance

        Args:
            connection: The desired connection instance
        """
        global _CONNECTION
        _CONNECTION = connection

    @property
    def pool(self) -> ThreadPoolExecutor:
        """The ThreadPoolExecutor that will contain all MAPI requests
        """
        if self._pool is None:
            self._pool = THREADPOOL or _create_threadpool()

        return self._pool

    @staticmethod
    def get_current_connection() -> MAPIConnection:
        """Get the current connection instance
        """
        return _CONNECTION or _create_default_connection()

    def __enter__(self) -> MAPIConnection:
        self._prev = _CONNECTION
        self._set_connection(self)
        return self

    def __exit__(self, type_, value, traceback):
        self._set_connection(self._prev)


_CONNECTION: Optional[MAPIConnection] = None


def _create_default_connection() -> MAPIConnection:
    """Creates the default MAPIConnection object
    """
    global _CONNECTION
    _CONNECTION = MAPIConnection()
    return _CONNECTION


ThreadedOutput = TypeVar('ThreadedOutput')


def run_in_threadpool(
    f: Callable[..., ThreadedOutput],
    *args: Any,
    connection: Optional[MAPIConnection] = None,
    **kwargs: Any,
) -> Future[ThreadedOutput]:
    """Run the provided function in the MAPI threadpool and return a Future

    Args:
        f: An arbitrary function
        *args, **kwargs: Arbitrary arguments with which to call ``f``
        connection: Optional :type MAPIConnection: whose threadpool will be used

    Returns:
        A Future for the return value of ``f``
    """
    if not connection:
        connection = MAPIConnection.get_current_connection()
    return connection.pool.submit(f, *args, **kwargs)


def run_kube_in_threadpool(
    f: Callable[..., ThreadedOutput],
    *args: Any,
    connection: Optional[MAPIConnection] = None,
    **kwargs: Any,
) -> Future[ThreadedOutput]:
    """Wrap a function that calls Kubernetes and returns a :type DeserializableModel: in
    a Future

    Args:
        f: Function that calls Kubernetes
        *args, **kwargs: Arbitrary arguments with which to call ``f``
        connection: Optional :type MAPIConnection: whose threadpool will be used

    Returns:
        A Future for the return value of ``f``
    """
    return run_in_threadpool(KubernetesException.wrap(f), *args, connection=connection, **kwargs)


ModelT = TypeVar('ModelT', bound=DeserializableModel)


def run_plural_mapi_request(
    query: str,
    query_function: str,
    return_model_type: Optional[Type[ModelT]] = None,
    variables: Optional[Dict[str, Any]] = None,
    connection: Optional[MAPIConnection] = None,
) -> Future[List[ModelT]]:
    """Run a GraphQL query against MAPI and return a future for a list of items

    Args:
        query: Query to run
        query_function: GraphQL endpoint for the query (e.g. 'createRun')
        return_model_type: The data type into which the response should be deserialized.
            Required if data is expected to be returned.
        variables: Variables to be passed to the GraphQL endpoint. Defaults to None.
        connection: The MAPI connection that should be used. Defaults to the connection
            returned by `MAPIConnection.get_current_connection()`.

    Returns:
        A `concurrent.futures.Future` for the request. You can retrieve the data using
        `future.result()` with an optional `timeout` argument.

    Raises:
        MAPIException: Raised if the request fails. See ``MAPIException`` for details on
        exception status codes
    """
    if not connection:
        connection = MAPIConnection.get_current_connection()

    future = connection.pool.submit(
        _threaded_plural_mapi_request,
        api_key=connection.api_key,
        endpoint=connection.endpoint,
        query=query,
        variables=variables,
        query_function=query_function,
        model_type=return_model_type,
    )
    future = cast('Future[List[ModelT]]', future)

    return future


def _threaded_plural_mapi_request(
    api_key: str,
    endpoint: str,
    query: str,
    variables: Optional[Dict[str, Any]],
    query_function: str,
    model_type: Optional[Type[ModelT]],
) -> List[ModelT]:
    """Run a graphql request in a thread and return a list of items
    """
    try:
        response = _run_graphql_request(api_key, endpoint, query, variables)
    except requests.exceptions.ConnectionError as e:
        mapi_error = MAPIException.from_requests_error(e)
        raise mapi_error from e

    deserialized: SuccessResponse[ModelT] = _deserialize_response(response, query_function, model_type)
    return deserialized.items


def run_singular_mapi_request(
    query: str,
    query_function: str,
    return_model_type: Optional[Type[ModelT]] = None,
    variables: Optional[Dict[str, Any]] = None,
    connection: Optional[MAPIConnection] = None,
) -> Future[ModelT]:
    """Run a GraphQL query against MAPI and return a future for a singular item

    Args:
        query: Query to run
        query_function: GraphQL endpoint for the query (e.g. 'createRun')
        return_model_type: The data type into which the response should be deserialized.
            Required if data is expected to be returned.
        variables: Variables to be passed to the GraphQL endpoint. Defaults to None.
        connection: The MAPI connection that should be used. Defaults to the connection
            returned by `MAPIConnection.get_current_connection()`.

    Returns:
        A `concurrent.futures.Future` for the request. You can retrieve the data using
        `future.result()` with an optional `timeout` argument.

    Raises:
        MAPIException: Raised if the request fails. See ``MAPIException`` for details on
        exception status codes
    """
    if not connection:
        connection = MAPIConnection.get_current_connection()

    future = connection.pool.submit(
        _threaded_singular_mapi_request,
        api_key=connection.api_key,
        endpoint=connection.endpoint,
        query=query,
        variables=variables,
        query_function=query_function,
        model_type=return_model_type,
    )
    future = cast('Future[ModelT]', future)

    return future


def _threaded_singular_mapi_request(
    api_key: str,
    endpoint: str,
    query: str,
    variables: Optional[Dict[str, Any]],
    query_function: str,
    model_type: Optional[Type[ModelT]],
) -> ModelT:
    """Run a graphql request in a thread and return a single item

    Raises:
        MAPIException: Raised if no items were found
    """

    items = _threaded_plural_mapi_request(
        api_key=api_key,
        endpoint=endpoint,
        query=query,
        variables=variables,
        query_function=query_function,
        model_type=model_type,
    )
    if len(items) == 1:
        return items[0]
    else:
        raise MAPIException(status=HTTPStatus.INTERNAL_SERVER_ERROR,
                            message='Request returned no items, but expected 1')


def run_empty_mapi_request(
    query: str,
    query_function: str,
    variables: Optional[Dict[str, Any]] = None,
    connection: Optional[MAPIConnection] = None,
) -> Future[None]:
    """Run a GraphQL query against MAPI a future for the response

    If the result succeeds, ``future.result()`` will return ``None``, otherwise it will
    error with a ``MAPIException``.

    Args:
        query: Query to run
        query_function: GraphQL endpoint for the query (e.g. 'createRun')
        variables: Variables to be passed to the GraphQL endpoint. Defaults to None.
        connection: The MAPI connection that should be used. Defaults to the connection
            returned by `MAPIConnection.get_current_connection()`.

    Returns:
        A `concurrent.futures.Future` for the request. You can retrieve the data using
        `future.result()` with an optional `timeout` argument.
    """
    if not connection:
        connection = MAPIConnection.get_current_connection()

    future = connection.pool.submit(
        _threaded_empty_mapi_request,
        api_key=connection.api_key,
        endpoint=connection.endpoint,
        query=query,
        variables=variables,
        query_function=query_function,
    )

    return future


def _threaded_empty_mapi_request(
    api_key: str,
    endpoint: str,
    query: str,
    variables: Optional[Dict[str, Any]],
    query_function: str,
) -> None:
    """Run a graphql request in a thread and return None if the request succeeded
    """

    _ = _threaded_plural_mapi_request(
        api_key=api_key,
        endpoint=endpoint,
        query=query,
        variables=variables,
        query_function=query_function,
        model_type=None,
    )


def _run_graphql_request(
    api_key: str,
    endpoint: str,
    query: str,
    variables: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:

    if variables is None:
        variables = {}
    variables = {key.replace('$', ''): value for key, value in variables.items()}

    headers = {
        'Content-Type': 'application/json',
        'authorization': api_key,
    }
    payload = json.dumps({'query': query, 'variables': variables})

    # Don't want timeout since this will be run in a background thread
    # pylint: disable-next=missing-timeout
    response = requests.request(
        'POST',
        endpoint,
        headers=headers,
        data=payload,
    )
    try:
        return response.json()
    except requests.JSONDecodeError as e:
        mapi_error = MAPIException.from_requests_error(e)
        raise mapi_error from e


def _deserialize_response(
    response: Dict[str, Any],
    query_function: str,
    model_type: Optional[Type[ModelT]],
) -> SuccessResponse[ModelT]:
    """Given response, function, and model object, deserializes data into SuccessResponse

    raises
        MAPIException: Something on the MAPI side went wrong (400s) or the
            response didn't match the expected format (500)
        MultiMAPIException: Multiple errors encountered in graphql
    """

    # Check response for errors in the header (typically 401/403)
    error_to_raise = [MAPIException.from_mapi_error_response(e) for e in response.get('errors', [])]
    if error_to_raise:
        raise MultiMAPIException(error_to_raise)

    # Parse reponse (raises 500 if cannot be parsed, 400s for status codes passed through data)
    try:
        data = response['data']
        query_response: Dict[str, Any] = data[query_function]
        raw_response = RawSuccessResponse(**query_response)
    except (KeyError, TypeError) as e:
        raise MAPIException(status=HTTPStatus.INTERNAL_SERVER_ERROR,
                            message='Internal Server Error: Malformed response data') from e

    # Convert response into model
    if model_type is None:
        return raw_response.empty_success
    else:
        # TODO: handle any errors with deserialization here
        return raw_response.deserialize(model_type)
