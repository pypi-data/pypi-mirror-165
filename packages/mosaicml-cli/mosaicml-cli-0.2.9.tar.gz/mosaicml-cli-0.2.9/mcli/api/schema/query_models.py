""" Automatic Deserialization for GraphQL Responses """
from dataclasses import dataclass, field
from http import HTTPStatus
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

import yaml

from mcli.api.exceptions import MAPIException
from mcli.api.schema.generic_model import DeserializableModel

ModelT = TypeVar('ModelT', bound=DeserializableModel)


@dataclass
class SuccessResponse(Generic[ModelT]):
    """Successful Response"""
    message: Optional[str] = None
    items: List[ModelT] = field(default_factory=list)

    def __str__(self) -> str:
        return 'SuccessResponse:\n' + ('-' * 40) + '\n' + yaml.dump(self.to_dict())

    def to_dict(self) -> Dict[str, Any]:
        """Converts the query into a dictionary
        """
        return {
            'message': self.message,
            'items': self.items,
        }


class RawSuccessResponse:
    """ Raw Success Response """
    status: HTTPStatus
    message: Optional[str] = None
    items: List[Dict[str, Any]] = []

    def __init__(
        self,
        status: int,
        message: Optional[str] = None,
        items: Optional[List[Dict[str, Any]]] = None,
        **kwargs: Dict[str, Any],
    ):
        """ An Raw Query Response that includes raw data

        Args:
            status: Required HTTPStatus code that can be used to determine if the
                query was successful
            message: An Optional[str] message, usually used for errors
            items: An Optional list of dictionary data which can be initialized into a
                List of DeserializedModel types
        """
        del kwargs

        self.status = HTTPStatus(status)
        self.message = message
        self.items = items or []

        if self.status >= 400:
            args: Dict[str, Any] = {'status': self.status}
            if self.message is not None:
                args['message'] = self.message
            raise MAPIException(**args)

    def __str__(self) -> str:
        return 'RawSuccessResponse:\n' + ('-' * 40) + '\n' + yaml.dump(self.to_dict())

    def to_dict(self) -> Dict[str, Any]:
        """Converts the query into a dictionary
        """
        return {
            'status': self.status.value,
            'message': self.message,
            'items': self.items,
        }

    @property
    def empty_success(self) -> SuccessResponse:
        return SuccessResponse(message=self.message, items=[])

    def deserialize(self, model_type: Type[ModelT]) -> SuccessResponse[ModelT]:
        translated_items: List[ModelT] = []
        for item in self.items:
            model_item = model_type.from_mapi_response(item)
            translated_items.append(model_item)

        return SuccessResponse(message=self.message, items=translated_items)
