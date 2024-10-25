from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def choose_role_kb():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Делегат", callback_data="reg_Делегат"))
    builder.row(InlineKeyboardButton(text="Гость", callback_data="reg_Гость"))
    return builder.as_markup()


def select_organize_kb():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Организатор", callback_data="reg_Организатор"))
    return builder.as_markup()
