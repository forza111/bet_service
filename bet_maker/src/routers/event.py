from fastapi import Depends, APIRouter
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependensies import get_async_session
from src.schemas.event import EventViewSchema
from src import crud


router = APIRouter()


@router.get("/events/", response_model=list[EventViewSchema])
async def get_events(
        limit: int = 10,
        offset: int = 0,
        session: AsyncSession = Depends(get_async_session)
):
    events = await crud.event.get_events(session, limit, offset)
    return events
