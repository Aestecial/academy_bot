from aiogram.fsm.state import State, StatesGroup


class ProgramsStates(StatesGroup):
    waiting_for_event_text = State()
    waiting_for_poll_choice = State()
    waiting_for_edit_choice = State()
    preview = State()
