"""Postgres module."""

from typing import Callable, Dict, Union

from dataclasses import dataclass
from threading import Lock

from spec.types import Request

import sqlalchemy as sa  # noqa
from sqlalchemy import sql # noqa


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)

from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL

from spec.types import Module

lock_state = Lock()

EngineExpected = Union[AsyncEngine, None]
SessionExpected = Union[Callable, None]


TypeModel = declarative_base()


class Model(TypeModel):
    """Model."""

    __abstract__ = True


@dataclass
class Postgres(Module):
    """Postgres module."""

    host: str = 'localhost'
    port: int = 5432

    database: str = 'test'

    user: str = 'postgres'
    password: str = 'postgres'

    session_options: Dict = None
    engine_options: Dict = None

    __driver__: str = 'postgresql+asyncpg'  # noqa

    __session__: SessionExpected = None

    @property
    def engine(self) -> EngineExpected:
        """Engine."""
        try:
            return getattr(self.app.state, 'pg_engine')
        except Exception as _exc:  # noqa
            pass

    @property
    def session_maker(self) -> Callable:
        """Engine."""
        try:
            return getattr(self.app.state, 'pg_session_maker')
        except Exception as _exc:  # noqa
            pass

    def db_uri(self) -> URL:
        """Database uri."""
        return URL.create(
            drivername=self.__driver__,
            host=self.host,
            database=self.database,
            username=self.user,
            password=self.password,
            port=self.port,
        )

    def _engine_options(self) -> Dict:
        """Engine options."""
        options = {
            'future': True,
            'encoding': 'utf8',
            'echo': self.app.spec.status.debug,
            'echo_pool': self.app.spec.status.debug,
            'paramstyle': 'named',
            'hide_parameters': not self.app.spec.status.debug,
            'pool_size': 24,  # pool size max connections
            'pool_timeout': 5,  # sec, wait free connection in pool
            'max_overflow': 20,
        }

        if self.engine_options:
            options.update(self.engine_options)

        return options

    def _session_options(self) -> Dict:
        """Session options."""

        options = {
            'future': True,
            'class_': AsyncSession,
            'autoflush': True,
            'expire_on_commit': True,
        }

        if self.engine_options:
            options.update(self.engine_options)

        return options

    async def prepare(self, scope):
        """Prepare postgres."""

        engine = create_async_engine(
            self.db_uri(),
            **self._engine_options(),
        )

        if not engine:
            return

        with lock_state:
            maker = sessionmaker(engine, **self._session_options())
            self.app.state.pg_engine = engine
            self.app.state.pg_session_maker = maker

    async def health(self, scope) -> bool:
        """Health postgres."""

        if self.engine:
            async with self.session_maker() as session:
                status = await session.scalar('SELECT 1;')
                return status == 1

    async def release(self, scope):
        """Release postgres."""
        if self.engine:
            await self.engine.dispose()

    async def create_tables(self):
        """Create tables."""

        async with self.engine.begin() as conn:
            await conn.run_sync(Model.metadata.drop_all)
            await conn.run_sync(Model.metadata.create_all)


async def db(request: Request) -> AsyncSession:
    """Dep async db session."""

    maker = getattr(request.app.state, 'pg_session_maker')

    async with maker() as session:
        yield session
