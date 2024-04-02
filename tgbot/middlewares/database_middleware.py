from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

from src.config.database.db_config import Session
from src.config.database.database import User


class DatabaseMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any]
    ) -> Any:
        db_session = Session()
        event_user = data['event_from_user']
        user = db_session.query(User).filter(User.id == event_user.id).first()

        if not user:
            user = User(id=event_user.id, full_name=event_user.full_name)
            db_session.add(user)
            db_session.commit()
        elif user.full_name != event_user.full_name:
            user.full_name = event_user.full_name
            db_session.commit()

        data['db_session'] = db_session

        result = await handler(event, data)

        db_session.close()

        return result
