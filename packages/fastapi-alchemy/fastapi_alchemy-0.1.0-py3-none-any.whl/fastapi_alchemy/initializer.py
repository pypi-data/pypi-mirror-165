from typing import Union

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_scoped_session,
)
from sqlalchemy.orm import sessionmaker

from fastapi_alchemy.context import get_session_context
from fastapi_alchemy.exceptions import NotInitializedException


class Initializer:
    def __init__(self):
        self._session = None

    @property
    def session(self) -> Union[AsyncSession, async_scoped_session]:
        return self._session

    def init(self, db_url: str, engine_args, session_args) -> None:
        engine = create_async_engine(db_url, **engine_args)
        async_session_factory = sessionmaker(bind=engine, **session_args)
        self._session: Union[AsyncSession, async_scoped_session] = async_scoped_session(
            session_factory=async_session_factory,
            scopefunc=get_session_context,
        )

    def validate(self) -> None:
        if self._session is None:
            raise NotInitializedException


SessionInitializer = Initializer()
session = SessionInitializer.session
