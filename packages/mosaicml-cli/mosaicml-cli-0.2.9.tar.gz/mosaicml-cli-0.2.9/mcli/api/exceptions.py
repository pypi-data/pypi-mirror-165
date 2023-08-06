"""Cloud exceptions thrown"""
from __future__ import annotations

import functools
import logging
from enum import Enum
from http import HTTPStatus
from typing import Any, Callable, Dict, Optional, Type, TypeVar, Union

import requests
from kubernetes.client.exceptions import ApiException

logger = logging.getLogger(__name__)

DEFAULT_MESSAGE = 'Unknown Error'


class MCLIConfigError(Exception):
    pass


class MAPIException(Exception):
    """Exceptions raised when a request to MAPI fails

    Args:
        status: The status code for the exception
        message: A brief description of the error
        description: An optional longer description of the error

    Details:
    MAPI responds to failures with the following status codes:
    - 400: The request was misconfigured or missing an argument. Double-check the API and try again
    - 401: User credentials were either missing or invalid. Be sure to set your API key before making a request
    - 403: User credentials were valid, but the requested action is not allowed
    - 404: Could not find the requested resource(s)
    - 409: Attempted to create an object with a name that already exists. Change the name and try again.
    - 500: Internal error in MAPI. Please report the issue
    - 503: MAPI or a subcomponent is currently offline. Please report the issue
    """
    status: HTTPStatus
    message: str
    description: Optional[str] = None

    def __init__(self, status: HTTPStatus, message: str = DEFAULT_MESSAGE, description: Optional[str] = None):
        super().__init__()
        self.status = status
        self.message = message
        self.description = description

    def __str__(self) -> str:
        error_message = f'Error {self.status.value}: {self.message}'

        if self.description:
            error_message = f'{error_message}. {self.description}'

        return error_message

    @classmethod
    def from_mapi_error_response(cls, error: Dict[str, Any]) -> MAPIException:
        """Initializes a new exception based on error dict from a MAPI response
        """
        extensions = error.get('extensions', {})
        code = extensions.get('code', HTTPStatus.INTERNAL_SERVER_ERROR)
        try:
            status = HTTPStatus(code)
        except ValueError:
            logger.debug(f'Unknown status code {code}. Setting to 500')
            status = HTTPStatus.INTERNAL_SERVER_ERROR

        message = error.get('message', DEFAULT_MESSAGE)

        # TODO: could potentially include extensions['stacktrace'] as description for 500s internally
        # From apollo docs, this could only be available in dev?

        return MAPIException(status=status, message=message)

    @classmethod
    def from_requests_error(cls, error: requests.exceptions.RequestException) -> MAPIException:
        """Initializes a new exception based on a requests RequestException
        """
        msg = 'Unable to connect'
        if error.args:
            con = error.args[0]
            try:
                # Try to get the destination we tried to connect to
                # if the app is fully not accessible
                source = f'http://{con.pool.host}:{con.pool.port}{con.url}'
            except AttributeError:
                # Not all RequestException have pool information, examples:
                #   1.  app is partially up but not fully responding
                #   2.  host is correct but full URL is not
                source = 'MAPI'
            msg = f'{msg} to {source}'
        return MAPIException(status=HTTPStatus.SERVICE_UNAVAILABLE, message=msg)


class MultiMAPIException(MAPIException):
    """Raises 1 or more MAPI Exceptions

    Graphql can technically return multiple errors in the response. This
    allows the user to see all of them at once rather than having to debug
    one by one
    """

    def __init__(self, errors: list[MAPIException]) -> None:
        self.errors = errors
        status = max(e.status for e in errors)
        super().__init__(status)

    def __str__(self) -> str:
        return "\n".join([str(x) for x in self.errors])


class KubernetesErrorDesc(Enum):
    """Provides descriptions for common Kubernetes errors that we might encounter
    """

    UNAUTHORIZED = 'Invalid cluster credentials: Please contact your cluster administrator'
    FORBIDDEN = 'Invalid permissions: The requested action is not allowed. Please contact your cluster administrator'
    NOT_FOUND = 'Object not found: Could not find the requested object'
    CONFLICT = 'Object already exists: Please ensure you are using unique names'
    UNPROCESSABLE_ENTITY = ('Submitted object misconfigured: This usually occurs when secrets and other objects '
                            'are duplicated. Please double-check and try again.')
    INTERNAL_SERVER_ERROR = ('Cluster error: The cluster seems to be struggling with something. '
                             'Please report this issue to your cluster administrator')


# pylint: disable-next=invalid-name
TFunc = TypeVar('TFunc', bound=Callable[..., Any])


class KubernetesException(MAPIException):
    """Exceptions raised when a Kubernetes request fails

    Args:
        status: The status code for the exception
        message: A brief description of the error
        description: An optional longer description of the error

    Details:
    Kubernetes will respond with a variety of status codes when a request fails. Below are some of the common ones:
    - 401: User credentials were invalid. Check with your cluster administrator on how to get new ones
    - 403: User credentials were valid, but the requested action is not allowed
    - 409: Attempted to create an object with a name that already exists. Change the name and try again.
    - 422: Submitted object misconfigured: This usually occurs when secrets and other objects
           are duplicated. Please double-check and try again.
    - 500: Internal cluster error. Please report the issue
    """

    @classmethod
    def transform_api_exception(
        cls: Type[KubernetesException],
        e: ApiException,
    ) -> Union[KubernetesException, ApiException]:

        try:
            status = HTTPStatus(e.status)
            message = KubernetesErrorDesc[status.name].value  # pylint: disable=no-member
        except (KeyError, TypeError):
            return e

        logger.debug(f'Transformed Kubernetes exception: {e}')
        return cls(status=status, message=message)

    @classmethod
    def wrap(cls, f: TFunc) -> TFunc:
        """Wrap the provided callable to catch any Kubernetes ApiException and
        throw a transformed KubernetesException

        Args:
            f: Callable that might raise an ApiException

        Raises:
            KubernetesException: Raised if an ApiException was hit that we know how to message to the user
            ApiException: Raised if an unfamiliar ApiException is hit

        Returns:
            A wrapped callable
        """

        @functools.wraps(f)
        def wrapped(*args: Any, **kwargs: Any):
            try:
                return f(*args, **kwargs)
            except ApiException as e:
                raise cls.transform_api_exception(e) from e

        return wrapped  # type: ignore
