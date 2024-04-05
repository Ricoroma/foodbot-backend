from typing import Type

from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.fsm.storage.base import StorageKey
from aiogram.utils.formatting import Text
from aiogram.filters import Command
from sqlalchemy.orm import Session

from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, FSInputFile
from aiogram.fsm.context import FSMContext

from src.config.database.database import User
from tgbot.keyboards.keyboards import main_kb

router = Router()


@router.message(Command('start'))
async def start_handler(message: Message):

    await message.answer('Добро пожаловать', reply_markup=main_kb())
