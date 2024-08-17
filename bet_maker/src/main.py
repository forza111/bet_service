import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from src.routers import bet, event
from src.rabbit.consumer import consume_queue
from src.crud.event import create_event, update_event


@asynccontextmanager
async def rabbitmq_consumer(app: FastAPI):
    asyncio.create_task(
        consume_queue(name_queue='create_event_queue', func=create_event)
    )
    asyncio.create_task(
        consume_queue(name_queue='update_event_queue', func=update_event)
    )
    yield


app = FastAPI(lifespan=rabbitmq_consumer)
app.include_router(
    bet.router,
    tags=["bets"],
)
app.include_router(
    event.router,
    tags=["events"],
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
