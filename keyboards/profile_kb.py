from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

# Определение классов callback data
from aiogram.filters.callback_data import CallbackData


class InventoryPageCallback(CallbackData, prefix="invpage"):
    page: int


class InventoryItemCallback(CallbackData, prefix="invitem"):
    item_id: int  # Заменяем item_name на item_id


def menu_profile_kb():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text='Добавить цель', callback_data='add_goal'))
    keyboard.row(InlineKeyboardButton(text='Изменить инициалы', callback_data='change_initials'))
    keyboard.row(InlineKeyboardButton(text='Изменить username', callback_data='change_username'))
    keyboard.row(InlineKeyboardButton(text='Покупки', callback_data='inventory'))
    keyboard.row(InlineKeyboardButton(text='Назад', callback_data='back_menu'))
    return keyboard.as_markup()


def add_goal_kb(goals_len: int):
    keyboard = InlineKeyboardBuilder()
    if goals_len < 5:
        keyboard.row(InlineKeyboardButton(text='Добавить новую цель', callback_data='add_new_goal'))
    if goals_len != 0:
        keyboard.row(InlineKeyboardButton(text='Удалить существующую цель', callback_data='delete_goal'))
    keyboard.row(InlineKeyboardButton(text='Назад', callback_data='profile'))
    return keyboard.as_markup()


def add_new_goal_kb():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text='Добавить', callback_data='create_new_goal'))
    keyboard.row(InlineKeyboardButton(text='Отменить', callback_data='add_goal'))
    return keyboard.as_markup()


def back_successful():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text='Вернуться', callback_data='add_goal'))
    return keyboard.as_markup()


def profile_back():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text='Вернуться', callback_data='profile'))
    return keyboard.as_markup()


def main_back():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text='Вернуться', callback_data='back_menu'))
    return keyboard.as_markup()


def delete_goal_kb(goals: list):
    keyboard = InlineKeyboardBuilder()
    for goal in goals:
        keyboard.row(InlineKeyboardButton(text=f"{goal[0]}", callback_data=f"forcedelete_{goal[0]}"))
    keyboard.row(InlineKeyboardButton(text='Вернуться', callback_data='add_goal'))
    return keyboard.as_markup()


def inventory_kb(items, page, total_pages):
    builder = InlineKeyboardBuilder()

    if items:
        for item in items:
            builder.button(
                text=item[1],  # item name
                callback_data=InventoryItemCallback(item_id=item[3]).pack()  # Используем item_id в callback data
            )
        builder.adjust(3)

    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(
            InlineKeyboardButton(text="<-", callback_data=InventoryPageCallback(page=page - 1).pack()))
    navigation_buttons.append(InlineKeyboardButton(text="Вернуться", callback_data="profile"))
    if page < total_pages:
        navigation_buttons.append(
            InlineKeyboardButton(text="->", callback_data=InventoryPageCallback(page=page + 1).pack()))

    builder.row(*navigation_buttons)

    return builder.as_markup()


# Функция для генерации клавиатуры инвентаря
def generate_inventory_keyboard(items, page, total_pages):
    builder = InlineKeyboardBuilder()
    if items:
        for item in items:
            builder.button(
                text=item[1],
                callback_data=InventoryItemCallback(item_id=item[-1]).pack()
            )
        builder.adjust(3)
    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(
            InlineKeyboardButton(text="<-", callback_data=InventoryPageCallback(page=page - 1).pack()))
    navigation_buttons.append(InlineKeyboardButton(text="Вернуться", callback_data="profile"))
    if page < total_pages:
        navigation_buttons.append(
            InlineKeyboardButton(text="->", callback_data=InventoryPageCallback(page=page + 1).pack()))
    builder.row(*navigation_buttons)
    return builder.as_markup()
