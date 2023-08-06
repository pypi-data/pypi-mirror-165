from uuid import uuid4

from fastapi_alchemy import SessionInitializer, session
from fastapi_alchemy.context import reset_session_context, set_session_context


class SQLAlchemyMiddleware:
    def __init__(self, app) -> None:
        self.app = app

    async def __call__(self, scope, receive, send) -> None:
        SessionInitializer.validate()
        session_id = str(uuid4())
        context = set_session_context(session_id=session_id)

        try:
            await self.app(scope, receive, send)
        except Exception as e:
            raise e
        finally:
            await session.remove()
            reset_session_context(context=context)
