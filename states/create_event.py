from aiogram.fsm.state import State, StatesGroup


class EventStates(StatesGroup):
    event_name = State()
    waiting_for_event_text = State()
    waiting_for_max_participants = State()
    preview = State()
    waiting_for_poll_choice = State()
    waiting_for_edit_choice = State()
