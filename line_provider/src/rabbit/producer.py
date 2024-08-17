import asyncio
from typing import Any

import aio_pika
from aio_pika.abc import AbstractRobustConnection, AbstractRobustChannel
from aio_pika.message import Message
import pydantic

from src.config import RMQ_LOGIN, RMQ_PASSWORD, RMQ_HOST
from src.rabbit.serializer import serialize_data


RABBITMQ_URL: str = f"amqp://{RMQ_LOGIN}:{RMQ_PASSWORD}@{RMQ_HOST}/"


class RabbitMQConnection:
    _connection: AbstractRobustConnection | None = None
    _channel: AbstractRobustChannel | None = None

    async def connect(self) -> None:
        """
        Connecting to broker

        :return: None
        """
        self._connection = await aio_pika.connect_robust(RABBITMQ_URL, loop=asyncio.get_event_loop())
        self._channel = await self._connection.channel()

    async def send(self, queue_name: str, data: Any, schema: type[pydantic.BaseModel]):
        """
        Sending message to queue

        :param queue_name: str
        :param data: Any
        :param schema: type[pydantic.BaseModel]
        :return: None
        """
        message = Message(
            body=serialize_data(data, schema),
            content_type="application/json",
        )
        await self._channel.declare_queue(queue_name, durable=True)
        await self._channel.default_exchange.publish(message, queue_name)


rabbit_connection = RabbitMQConnection()