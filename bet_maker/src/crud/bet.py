import datetime

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import models
from src.schemas.bet import BetCreateSchema


async def create_bet(
        session: AsyncSession,
        bet: BetCreateSchema
):
    select_stmt = sa.select(models.Event).where(models.Event.id == bet.event_id)
    event = (await session.scalars(select_stmt)).one_or_none()
    if event is None:
        return
    if event.state != 'NEW':
        return
    if event.deadline < datetime.datetime.now(datetime.timezone.utc):
        return
    insert_stmt = (
        sa.insert(models.Bet).values(
            **bet.model_dump(),
            coefficient=event.coefficient,
        ).returning(models.Bet)
    )
    result = (await session.scalars(insert_stmt)).one()
    await session.commit()
    return result


async def get_bets(
        session: AsyncSession,
        limit: int = 10,
        offset: int = 0
):
    select_stmt = sa.select(models.Bet).limit(limit).offset(offset)
    result = (await session.scalars(select_stmt)).all()
    return result
