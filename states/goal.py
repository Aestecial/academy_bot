from aiogram.fsm.state import StatesGroup, State


class GoalState(StatesGroup):
    waiting_for_message = State()
