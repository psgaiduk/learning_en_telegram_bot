from pydantic.generics import GenericModel
from typing import TypeVar, Generic

DataT = TypeVar('DataT')


class OneResponseDTO(GenericModel, Generic[DataT]):
    """One response DTO."""

    detail: DataT
