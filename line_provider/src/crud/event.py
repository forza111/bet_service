import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import models
from src.schemas.event import EventCreateSchema, EventUpdateSchema


async def get_event(session: AsyncSession, event_id: int):
    select_stmt = sa.select(models.Event).where(models.Event.id == event_id)
    result = (await session.scalars(select_stmt)).one_or_none()
    return result


async def get_events(
        session: AsyncSession,
        limit: int = 10,
        offset: int = 0
):
    select_stmt = sa.select(models.Event).limit(limit).offset(offset)
    result = (await session.scalars(select_stmt)).all()
    return result


async def create_event(
        session: AsyncSession,
        event: EventCreateSchema
):
    insert_stmt = (
        sa.insert(models.Event).values(event.model_dump()).returning(
            models.Event)
    )
    result = (await session.scalars(insert_stmt)).one()
    await session.commit()
    return result


async def update_event(
        event_id: id,
        event: EventUpdateSchema,
        session: AsyncSession,
):
    updates = event.model_dump(exclude_none=True)
    update_stmt = sa.update(models.Event).where(
        models.Event.id == event_id
    ).values(**updates).returning(models.Event)
    result = (await session.scalars(update_stmt)).one_or_none()
    await session.commit()
    return result
