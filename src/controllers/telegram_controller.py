from typing import Annotated, List

from aiogram import Dispatcher, Bot
from aiogram.types import Update
from fastapi import Depends, HTTPException, Query, APIRouter
from sqlalchemy.orm import Session
from ..config.database.database import MenuOption, User, sqlalchemy_to_pydantic, Cart, PositionInCart
from ..config.project_config import token
from ..support.dependencies import get_session
from ..support.schemas import MenuOptionModel, UpdateCartRequest, CartModel

router = APIRouter()

dp = Dispatcher()
bot = Bot(token=token)


@router.post(f"/hook")
async def process_event(update: Update):
    try:
        await dp.feed_webhook_update(bot=bot, update=update)
        return {"ok": True}
    except Exception as e:
        print(e)
