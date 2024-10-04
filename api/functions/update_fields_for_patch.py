from typing import Generic, TypeVar

T = TypeVar("T")


def patch_data(object_from_db: T, request: Generic[T]) -> T:
    """Patch data from request to object from db."""

    for field_name, field_value in vars(request).items():
        if field_value is not None:
            setattr(object_from_db, field_name, field_value)

    return object_from_db
