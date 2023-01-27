from aiogram.fsm.state import StatesGroup, State


class Dialog(StatesGroup):
    session = State()
    password = State()
