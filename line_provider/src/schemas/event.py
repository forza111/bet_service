import decimal
from enum import Enum
from typing import Optional, Annotated, Any

from pydantic import BaseModel, Field, AwareDatetime, model_validator


Coefficient = Annotated[decimal.Decimal, Field(ge=0.01, decimal_places=2)]


class EventState(str, Enum):
    NEW = "NEW"
    WIN_FIRST = "WIN_FIRST"
    WIN_SECOND = "WIN_SECOND"


class EventCreateSchema(BaseModel):
    coefficient: Coefficient
    deadline: AwareDatetime
    state: EventState


class EventUpdateSchema(BaseModel):
    coefficient: Optional[Coefficient] = None
    deadline: Optional[AwareDatetime] = None
    state: Optional[EventState] = None

    @model_validator(mode="before")
    @classmethod
    def _has_at_least_one_field(cls, data: Any) -> Any:
        intersection = list(
            set(data.keys()).intersection(set(cls.model_fields.keys()))
        )
        if not intersection:
            raise ValueError('There is no data to update')
        return data


class EventViewSchema(EventCreateSchema):
    id: int
