from aiogram.fsm.state import StatesGroup, State


class CoinsStates(StatesGroup):
    waiting_for_message = State()
