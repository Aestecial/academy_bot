from aiogram.fsm.state import StatesGroup, State


class InitialsState(StatesGroup):
    change_initials = State()
