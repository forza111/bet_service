import asyncio


from src.db.models import Base
from src.db.database import async_engine

async def create_tables(drop_exists: bool = False):
    async with async_engine.begin() as conn:
        if drop_exists:
            await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


