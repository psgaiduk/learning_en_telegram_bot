from pydantic.generics import GenericModel
from typing import TypeVar, Generic

DataT = TypeVar('DataT')


class PaginatedResponseDTO(GenericModel, Generic[DataT]):
    """Paginated response DTO."""

    results: list[DataT]
    page: int
    per_page: int
    total: int
    total_pages: int
