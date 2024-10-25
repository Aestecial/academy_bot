from aiogram.fsm.state import StatesGroup, State


class MailingState(StatesGroup):
    waiting_for_message = State()
