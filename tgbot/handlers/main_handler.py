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
