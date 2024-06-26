from typing import Type

from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.fsm.storage.base import StorageKey
from aiogram.utils.formatting import Text
from aiogram.filters import Command
from sqlalchemy.orm import Session

from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, FSInputFile, URLInputFile
from aiogram.fsm.context import FSMContext

from src.config.database.database import User, Category
from tgbot.filters.is_adm import IsAdmin
from tgbot.keyboards.admin_keyboards import *
from tgbot.utils.states import AdminState

router = Router()
router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())


@router.message(Command('admin'))
async def start_handler(message: Message):
    await message.answer('Добро пожаловать', reply_markup=main_adm_kb())


@router.callback_query(F.data == 'categories')
@router.message(F.text == 'Категории')
async def admin_categories_handler(update: Message | CallbackQuery, state: FSMContext, db_session: Session):
    await state.clear()

    categories = db_session.query(Category).all()

    if isinstance(update, Message):
        func = update.answer
    else:
        func = update.message.edit_text

    await func('Выберите категорию для продолжения', reply_markup=categories_kb(categories))


@router.callback_query(F.data.startswith('category:'))
async def admin_show_category(call: CallbackQuery, db_session: Session):
    cat_id = int(call.data.split(':')[1])

    category: Category = db_session.query(Category).get(cat_id)

    await call.message.edit_text(
        f'Категория {category.name}\nОписание: {category.description}',
        reply_markup=category_kb(cat_id)
    )


@router.callback_query(F.data.startswith('change_category:'))
async def admin_change_category_start(call: CallbackQuery, state: FSMContext):
    cat_id, param = call.data.split(':')[1:]
    cat_id = int(cat_id)

    await state.update_data(cat_id=cat_id, param=param)
    await state.set_state(AdminState.change_category)

    await call.message.answer('Введите новое значение', reply_markup=cancel_kb())
    await call.answer()


@router.callback_query(F.data.startswith('delete_category:'))
async def admin_delete_category_start(call: CallbackQuery, state: FSMContext, db_session: Session):
    cat_id = call.data.split(':')[1]
    cat_id = int(cat_id)

    category: Category = db_session.query(Category).get(cat_id)

    await call.message.edit_text(
        f'Вы уверены, что хотите удалить категорию {category.name}? '
        f'Это также затронет все товары, относящиеся к ней',
        reply_markup=confirm_delete_kb(cat_id, 'category')
    )


@router.callback_query(F.data.startswith('confirm_delete'))
async def admin_delete_category(call: CallbackQuery, state: FSMContext, db_session: Session):
    type, id = call.data.split(':')[1:]
    id = int(id)

    if type == 'category':
        category: Category = db_session.query(Category).get(id)
        for menu_option in category.menu_options:
            db_session.delete(menu_option)
        db_session.delete(category)
        db_session.commit()

        categories = db_session.query(Category).all()
        await call.message.answer('<i>Категория удалена</i>', reply_markup=ReplyKeyboardRemove())
        await call.message.edit_text('Выберите категорию для продолжения', reply_markup=categories_kb(categories))


@router.callback_query(F.data == 'cancel')
async def cancel_action(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.answer('Действие отменено')
    await call.message.delete()


@router.message(AdminState.change_category)
async def admin_change_category(message: Message, state: FSMContext, db_session: Session):
    data = await state.get_data()
    cat_id = int(data['cat_id'])
    param = str(data['param'])

    db_session.query(Category).filter(Category.id == cat_id).update({param: message.text})
    db_session.commit()

    category: Category = db_session.query(Category).get(cat_id)

    await message.answer(
        f'Категория {category.name}\nОписание: {category.description}',
        reply_markup=category_kb(cat_id)
    )
    await state.clear()


@router.callback_query(F.data == 'new_cat')
async def new_category_handler(call: CallbackQuery, state: FSMContext):
    await call.answer()

    await call.message.answer('Введите название категории', reply_markup=back())
    await state.set_state(AdminState.add_category)


@router.message(AdminState.add_category)
async def process_add_category(message: Message, state: FSMContext, db_session: Session):
    data = await state.get_data()

    if not data.get('name', None):
        if message.text == '⬅️ Назад':
            categories = db_session.query(Category).all()
            await message.answer('Выберите категорию для продолжения', reply_markup=categories_kb(categories))

            await state.clear()
            return

        await state.update_data(name=message.text)
        await message.answer('Введите описание категории', reply_markup=back())
        return

    if not data.get('description', None):
        if message.text == '⬅️ Назад':
            await message.answer('Введите название категории', reply_markup=back())
            await state.update_data(name=None)
            return

        await state.update_data(description=message.text)

    await message.answer(
        f'<b>Добавление категории</b>\nНазвание: {data["name"]}\nОписание: {message.text}',
        reply_markup=confirm_create_category_kb()
    )

    await state.set_state(AdminState.confirm_create_category)


@router.message(AdminState.confirm_create_category)
async def create_category_handler(message: Message, state: FSMContext, db_session: Session):
    if message.text == '✅ Создать категорию':
        data = await state.get_data()
        db_session.add(Category(name=data['name'], description=data['description']))
        db_session.commit()

        categories = db_session.query(Category).all()
        await message.answer('<i>Категория добавлена</i>', reply_markup=ReplyKeyboardRemove())
        await message.answer('Выберите категорию для продолжения', reply_markup=categories_kb(categories))

    elif message.text == '⬅️ Назад':
        await state.update_data(description=None)
        await message.answer('Введите описание категории', reply_markup=back())
        await state.set_state(AdminState.add_category)
        return


@router.callback_query(F.data == 'positions')
@router.message(F.text == 'Позиции меню')
async def admin_positions_handler(update: Message | CallbackQuery, state: FSMContext, db_session: Session):
    await state.clear()

    categories = db_session.query(Category).all()

    if isinstance(update, Message):
        func = update.answer
    else:
        func = update.message.edit_text

    await func('Выберите категорию для продолжения', reply_markup=categories_kb(categories))


@router.callback_query(F.data.startswith('pos_category:'))
async def admin_show_category(call: CallbackQuery, db_session: Session, state: FSMContext):
    cat_id = int(call.data.split(':')[1])

    category: Category = db_session.query(Category).get(cat_id)

    await call.message.edit_text(
        f'Категория {category.name}\nПозиции:',
        reply_markup=positions_kb(category.menu_options)
    )

    await state.update_data(cat_id=cat_id)


@router.callback_query(F.data.startswith('position:'))
async def admin_show_category(call: CallbackQuery, db_session: Session, state: FSMContext):
    data = await state.get_data()
    cat_id = data['cat_id']

    pos_id = int(call.data.split(':')[1])

    position: MenuOption = db_session.query(MenuOption).get(pos_id)

    await call.message.delete()
    await call.message.answer_photo(URLInputFile(position.img_source))
