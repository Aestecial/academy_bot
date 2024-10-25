from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


def delete_guest_kb():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text='Удалить', callback_data=f'deleted_guest'))
    keyboard.row(InlineKeyboardButton(text='Вернуться', callback_data='back_menu'))
    return keyboard.as_markup()
