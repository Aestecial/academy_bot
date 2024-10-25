from aiogram.utils.keyboard import InlineKeyboardBuilder


def programs_kb():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Сменить", callback_data='update_programs')
    keyboard.button(text="Вернуться", callback_data='back_menu')
    return keyboard.as_markup()


def preview_kb():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Отправить", callback_data='send_programs')
    keyboard.button(text="Отмена", callback_data='cancel_programs')
    return keyboard.as_markup()
