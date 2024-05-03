from aiogram.fsm.state import StatesGroup, State


class AdminState(StatesGroup):
    change_category = State()
    add_category = State()
