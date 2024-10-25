from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class ItemCallback(CallbackData, prefix="item"):
    action: str
    item_id: str


class PageCallback(CallbackData, prefix="page"):
    page: int


def generate_shop_keyboard(items, page, total_pages, is_organizer):
    builder = InlineKeyboardBuilder()

    # Добавление предметов в клавиатуру
    for item in items:
        builder.button(
            text=item[0],
            callback_data=ItemCallback(action="view", item_id=str(item[-1])).pack()
        )

    builder.adjust(3)

    # Кнопка добавления предметов для организаторов
    if is_organizer:
        builder.row(InlineKeyboardButton(text="Добавить предмет", callback_data="add_item"))

    # Навигационные кнопки
    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(
            InlineKeyboardButton(text="<-", callback_data=PageCallback(page=page - 1).pack()))
    navigation_buttons.append(InlineKeyboardButton(text="Вернуться", callback_data="back_menu"))
    if page < total_pages:
        navigation_buttons.append(
            InlineKeyboardButton(text="->", callback_data=PageCallback(page=page + 1).pack()))

    builder.row(*navigation_buttons)

    return builder.as_markup()
