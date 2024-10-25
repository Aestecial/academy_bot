# Импортируем необходимые классы из библиотеки aiogram
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Функция для создания клавиатуры с кнопками в зависимости от роли пользователя
def start_kb(role: str = None):
    # Создаем объект для построения inline клавиатуры
    builder = InlineKeyboardBuilder()

    # Добавляем первую строку кнопок, доступную для всех ролей
    builder.row(InlineKeyboardButton(text='Пульс', callback_data='pulse'),
                InlineKeyboardButton(text='Программа', callback_data='programs'))

    # Если роль пользователя - Организатор
    if role == 'Организатор':
        # Добавляем кнопки, специфичные для организатора
        builder.row(InlineKeyboardButton(text='Записи мероприятия', callback_data='check_application'))
        builder.row(InlineKeyboardButton(text='Создать рассылку', callback_data='create_mailing'),
                    InlineKeyboardButton(text='Создать программу', callback_data='create_programs'))
        builder.row(InlineKeyboardButton(text='Профиль делегатов', callback_data='delegate_interaction'),
                    InlineKeyboardButton(text='Рейтинг делегатов', callback_data='delegate_rating'))
        builder.row(InlineKeyboardButton(text='Магазин', callback_data='shop'))

    # Если роль пользователя - Делегат
    elif role == 'Делегат':
        # Добавляем кнопки, специфичные для делегата
        builder.row(InlineKeyboardButton(text='Мой профиль', callback_data='profile'),
                    InlineKeyboardButton(text='Магазин', callback_data='shop'))
        builder.row(InlineKeyboardButton(text='Написать организаторам', callback_data='write_organizer'))

    # Если роль пользователя не указана или любая другая
    else:
        # Добавляем кнопки, доступные для этих пользователей
        builder.row(InlineKeyboardButton(text='Написать организаторам', callback_data='write_organizer'))
        builder.row(InlineKeyboardButton(text='Рейтинг делегатов', callback_data='delegate_rating'))
        builder.row(InlineKeyboardButton(text='Удалить аккаунт', callback_data='delete_yourself'))

    # Возвращаем готовую разметку inline клавиатуры
    return builder.as_markup()
