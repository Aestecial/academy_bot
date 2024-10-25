from aiogram.fsm.state import StatesGroup, State


class WriteStates(StatesGroup):
    waiting_for_message = State()
