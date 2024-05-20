from typing import Optional, Type
from typing import List

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from src.config.database.database import Category, MenuOption


def main_adm_kb():
    builder = ReplyKeyboardBuilder()

    builder.button(text='Категории')
    builder.button(text='Позиции меню')

    return builder.as_markup(resize_keyboard=True)


def categories_kb(categories: list[Type[Category]]):
    builder = InlineKeyboardBuilder()

    builder.add(*[InlineKeyboardButton(text=i.name, callback_data=f'category:{i.id}') for i in categories])

    builder.button(text='Новая категория', callback_data='new_cat')
    builder.button(text='⬅️ Назад', callback_data='main_admin')

    return builder.adjust(1).as_markup()


def category_kb(cat_id):
    builder = InlineKeyboardBuilder()

    builder.button(text='Изменить название', callback_data=f'change_category:{cat_id}:name')
    builder.button(text='Изменить описание', callback_data=f'change_category:{cat_id}:description')
    builder.button(text='🗑 Удалить', callback_data=f'delete_category:{cat_id}')

    builder.button(text='⬅️ Назад', callback_data='categories')


def confirm_delete_kb(id, type):
    builder = InlineKeyboardBuilder()

    builder.button(text='✅ Удалить', callback_data=f'confirm_delete:{type}:{id}')
    builder.button(text='❌ Отмена', callback_data=f'{type}:{id}')

    return builder.as_markup()


def back_category_kb(cat_id):
    builder = InlineKeyboardBuilder()

    builder.button(text='⬅️ Назад', callback_data=f'category:{cat_id}')

    return builder.as_markup()


def positions_kb(positions: list[MenuOption]):
    builder = InlineKeyboardBuilder()

    builder.add(*[InlineKeyboardButton(text=i.name, callback_data=f'position:{i.id}') for i in positions])

    builder.button(text='Новая позиция меню', callback_data='new_pos')
    builder.button(text='⬅️ Назад', callback_data='main_admin')

    return builder.adjust(1).as_markup()


def position_kb(pos_id):
    builder = InlineKeyboardBuilder()

    builder.button(text='Изменить название', callback_data=f'change_position:{pos_id}:name')
    builder.button(text='Изменить описание', callback_data=f'change_position:{pos_id}:description')
    builder.button(text='Изменить категорию', callback_data=f'change_position:{pos_id}:category')
    builder.button(text='Изменить цену', callback_data=f'change_position:{pos_id}:price')
    builder.button(text='Изменить метку', callback_data=f'change_position:{pos_id}:note')
    builder.button(text='Изменить картинку', callback_data=f'change_position:{pos_id}:img_source')
    builder.button(text='🗑 Удалить', callback_data=f'delete_position:{pos_id}')

    builder.button(text='⬅️ Назад', callback_data='categories')

    return builder.adjust(1).as_markup()


def back_positions_kb(pos_id):
    builder = InlineKeyboardBuilder()

    builder.button(text='⬅️ Назад', callback_data=f'position:{pos_id}')

    return builder.as_markup()


def cancel_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text='❌ Отмена', callback_data=f'cancel')

    return builder.as_markup()


def back():
    builder = ReplyKeyboardBuilder()

    builder.button(text='⬅️ Назад')

    return builder.as_markup(resize_keyboard=True)


def confirm_create_category_kb():
    builder = ReplyKeyboardBuilder()

    builder.add(
        KeyboardButton(text='✅ Создать категорию'),
        KeyboardButton(text='⬅️ Назад')
    )

    return builder.adjust(1).as_markup(resize_keyboard=True)
