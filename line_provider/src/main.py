from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from src.routers import event
from src.rabbit.producer import rabbit_connection


@asynccontextmanager
async def rabbitmq_producer(app: FastAPI):
    await rabbit_connection.connect()
    yield


app = FastAPI(lifespan=rabbitmq_producer)
app.include_router(
    event.router,
    tags=["events"],
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
