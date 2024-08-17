from fastapi import Depends, APIRouter
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependensies import get_async_session
from src.schemas.bet import BetCreateSchema, BetViewSchema
from src import crud


router = APIRouter()


@router.post("/bet/", response_model=BetCreateSchema)
async def create_bet(
        payload: BetCreateSchema,
        session: AsyncSession = Depends(get_async_session)
):
    """Creating bet"""
    bet = await crud.bet.create_bet(session, payload)
    if bet is None:
        raise HTTPException(
            status_code=404, detail="Bet on event is not available"
        )
    return bet


@router.get("/bets/", response_model=list[BetViewSchema])
async def get_bets(
        limit: int = 10,
        offset: int = 0,
        session: AsyncSession = Depends(get_async_session)
):
    """Returning all bets"""
    bets = await crud.bet.get_bets(session, limit, offset)
    return bets
