from typing import Optional
from typing import List

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def main_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text='Открыть меню', web_app=WebAppInfo(url='https://shop.ricoroma.ru/docs'))

    return builder.as_markup()
