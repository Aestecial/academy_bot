from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def write_organizer_kb():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text='Отправить организаторам', callback_data='send_organizers'))
    keyboard.row(InlineKeyboardButton(text='Отмена', callback_data='cancel_write_organizer'))
    return keyboard.as_markup()
