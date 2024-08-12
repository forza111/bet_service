from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME


class Base(DeclarativeBase):
    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f'{col}={getattr(self, col)}')
        return f"<{self.__class__.__name__} {','.join(cols)}>"


ASYNC_DB_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}' \
             f'@{DB_HOST}:{DB_PORT}/{DB_NAME}'
async_engine = create_async_engine(
    ASYNC_DB_URL,
    echo=True,
    future=True,
)
async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)
