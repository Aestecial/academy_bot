from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def mailing_kb():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text='Организаторам', callback_data='mailing_Организатор'),
        InlineKeyboardButton(text='Делегатам', callback_data='mailing_Делегат')
    )
    keyboard.row(
        InlineKeyboardButton(text='Гостям', callback_data='mailing_Гость'),
        InlineKeyboardButton(text='Всем', callback_data='mailing_Все')
    )
    keyboard.row(InlineKeyboardButton(text='Отмена', callback_data='cancel_mailing'))
    return keyboard.as_markup()


def redact_kb():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text='Начать рассылку', callback_data='start_mailing'))
    keyboard.row(InlineKeyboardButton(text='Изменить', callback_data='redact_mailing'))
    keyboard.row(InlineKeyboardButton(text='Отмена', callback_data='cancel_mailing'))
    return keyboard.as_markup()


def delegate_level():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text='1', callback_data='delegate/1'))
    keyboard.row(InlineKeyboardButton(text='2', callback_data='delegate/2'))
    keyboard.row(InlineKeyboardButton(text='3', callback_data='delegate/3'))
    keyboard.row(InlineKeyboardButton(text='Всем', callback_data='delegate/Всем'))
    keyboard.adjust(3, 1)
    return keyboard.as_markup()
