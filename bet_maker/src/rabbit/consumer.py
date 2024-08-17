import asyncio
from typing import Callable, Awaitable

import aio_pika
from aio_pika.message import IncomingMessage
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import RMQ_LOGIN, RMQ_PASSWORD, RMQ_HOST
from src.db.database import async_session_factory


RABBITMQ_URL: str = f"amqp://{RMQ_LOGIN}:{RMQ_PASSWORD}@{RMQ_HOST}/"


async def consume_queue(
        name_queue: str,
        func: Callable[[IncomingMessage, AsyncSession], Awaitable]
):
    connection: aio_pika.abc.AbstractRobustConnection = await (
        aio_pika.connect_robust(RABBITMQ_URL, loop=asyncio.get_event_loop())
    )
    async with connection:
        channel: aio_pika.abc.AbstractRobustChannel = \
            await connection.channel()
        queue: aio_pika.abc.AbstractRobustQueue = \
            await channel.declare_queue(name_queue, durable=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    async with async_session_factory() as session:
                        await func(message, session)
