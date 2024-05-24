from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from aiogram.types import Update
from fastapi import APIRouter
from ..config.project_config import token

router = APIRouter()

dp = Dispatcher()
bot = Bot(token=token, parse_mode=ParseMode.HTML)


@router.post(f"/hook")
async def process_event(update: Update):
    try:
        await dp.feed_webhook_update(bot=bot, update=update)
        return {"ok": True}
    except Exception as e:
        print(e)
