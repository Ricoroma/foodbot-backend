from aiogram.fsm.state import StatesGroup, State


class AdminState(StatesGroup):
    change_category = State()
    add_category = State()
    confirm_create_category = State()
