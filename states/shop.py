from aiogram.fsm.state import State, StatesGroup


class AddItem(StatesGroup):
    waiting_for_name = State()
    waiting_for_description = State()
    waiting_for_price = State()
    waiting_for_amount = State()
    waiting_for_photo = State()


class EditItem(StatesGroup):
    waiting_for_new_amount = State()
