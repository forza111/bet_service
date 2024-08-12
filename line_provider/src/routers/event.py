from fastapi import Depends, APIRouter
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependensies import get_async_session
from src.schemas.event import EventViewSchema, EventCreateSchema, EventUpdateSchema
from src import crud
# from src.rabbit.server import mq
from src.rabbit.producer import rabbit_connection

router = APIRouter()


@router.get("/event/", response_model=EventViewSchema)
async def get_event(
        event_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    event = await crud.event.get_event(session, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.get("/events/", response_model=list[EventViewSchema])
async def get_events(
        limit: int = 10,
        offset: int = 0,
        session: AsyncSession = Depends(get_async_session)
):
    events = await crud.event.get_events(session, limit, offset)
    return events


@router.post("/event/", response_model=EventViewSchema)
async def create_event(
        payload: EventCreateSchema,
        session: AsyncSession = Depends(get_async_session)
):
    event = await crud.event.create_event(session, payload)
    await rabbit_connection.send("create_event_queque", event, EventViewSchema)
    return event


@router.patch("/event/{event_id}", response_model=EventViewSchema)
async def update_event(
        event_id: int,
        payload: EventUpdateSchema,
        session: AsyncSession = Depends(get_async_session)
):
    updated_event = await crud.event.update_event(event_id, payload, session)
    if updated_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    await rabbit_connection.send("update_event_queque", updated_event, EventViewSchema)
    return updated_event
