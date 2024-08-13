import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from aio_pika.message import IncomingMessage

from src.db import models
from src.schemas.event import EventCreateSchema, EventUpdateSchema, EventState


async def create_event(message: IncomingMessage, session: AsyncSession) -> None:
    event = EventCreateSchema.model_validate_json(message.body)
    insert_stmt = (
        sa.insert(models.Event).values(event.model_dump()).returning(
            models.Event)
    )
    result = (await session.scalars(insert_stmt)).one()
    await session.commit()
    return result


async def update_event(
        message: IncomingMessage,
        session: AsyncSession,
) -> None:
    event = EventUpdateSchema.model_validate_json(message.body)
    updates = event.model_dump(exclude_none=True)
    event_id = updates.get('id')
    update_stmt = sa.update(models.Event).where(
        models.Event.id == event_id
    ).values(**updates).returning(models.Event)
    updated_event = (await session.scalars(update_stmt)).one_or_none()
    if updated_event is None:
        await session.rollback()
        raise ValueError('Event not found')
    if updated_event.state != EventState.NEW:
        await calculate_bets(updated_event, session)
    await session.commit()


async def calculate_bets(event, session: AsyncSession):
    update_stmt = (
        sa.update(models.Bet)
        .where(models.Bet.event_id == event.id)
        .where(models.Bet.match_outcome == event.state)
        .values(amount_of_winnings=models.Bet.coefficient*models.Bet.bet_amount)
    )
    await session.execute(update_stmt)


async def get_events(
        session: AsyncSession,
        limit: int = 10,
        offset: int = 0
):
    select_stmt = sa.select(models.Event).limit(limit).offset(offset)
    result = (await session.scalars(select_stmt)).all()
    await session.commit()
    return result
