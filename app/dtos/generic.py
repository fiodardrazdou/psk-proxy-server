from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

DataT = TypeVar("DataT")


class SingleMeta(BaseModel):
    status: str = "ok"


class SuccessResponse(GenericModel, Generic[DataT]):
    """
    A generic success response. Use like:
    """

    data: Optional[DataT]
    meta: dict = Field(
        default_factory=lambda: {
            "status": "ok",
        },
    )
