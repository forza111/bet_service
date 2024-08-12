import decimal
from enum import Enum
from typing import Optional, Annotated, Any

from pydantic import BaseModel, Field, AwareDatetime, model_validator


Amount = Annotated[decimal.Decimal, Field(ge=0.01, decimal_places=2)]


class MatchOutcome(str, Enum):
    WIN_FIRST = "WIN_FIRST"
    WIN_SECOND = "WIN_SECOND"


class BetCreateSchema(BaseModel):
    event_id: int
    match_outcome: MatchOutcome
    bet_amount: Amount


class BetViewSchema(BetCreateSchema):
    id: int
    coefficient: Amount
    amount_of_winnings: Optional[Amount]