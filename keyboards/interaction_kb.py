from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def generate_delegates(page: int, page_size: int = 9, delegates: list = None):
    start = (page - 1) * page_size
    end = start + page_size
    return delegates[start:end]


def interactive_kb(page: int, delegates: list):
    keyboard = InlineKeyboardBuilder()
    current_delegates = generate_delegates(page, delegates=delegates)
    for delegate in current_delegates:
        keyboard.row(
            InlineKeyboardButton(text=delegate[-1], callback_data=f'getdelegate_{delegate[1]}_{page}')
        )
    keyboard.adjust(3)

    # Navigation buttons
    if page * 9 < len(delegates) and page > 1:
        keyboard.row(
            InlineKeyboardButton(text="<-", callback_data=f'left_{page - 1}'),
            InlineKeyboardButton(text="->", callback_data=f'right_{page + 1}'),
        )
    elif page > 1:
        keyboard.row(
            InlineKeyboardButton(text="<-", callback_data=f'left_{page - 1}'),
        )
    elif page * 9 < len(delegates):
        keyboard.row(
            InlineKeyboardButton(text="->", callback_data=f'right_{page + 1}'),
        )
    keyboard.row(
        InlineKeyboardButton(text='Вернуться', callback_data=f'back_menu')
    )
    return keyboard.as_markup()


def delegate_interaction_kb(profile_id, current_page):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text='Добавить рейтинг', callback_data=f'add_rating_{profile_id}_{current_page}'))
    keyboard.row(InlineKeyboardButton(text='Сменить уровень', callback_data=f'set_level_{profile_id}_{current_page}'))
    keyboard.row(
        InlineKeyboardButton(text='Управление монетами', callback_data=f'add_coin_{profile_id}_{current_page}'))
    keyboard.row(
        InlineKeyboardButton(text='Удалить делегата', callback_data=f'remove_delegate_{profile_id}_{current_page}'))
    keyboard.row(InlineKeyboardButton(text='Вернуться', callback_data=f'delegate_interaction/{current_page}'))
    return keyboard.as_markup()


def main_profile_back(profile_id, current_page):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text='Вернуться', callback_data=f'getdelegate_{profile_id}_{current_page}'))
    return keyboard.as_markup()


def add_rating_kb(profile_id, current_page):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text='⭐️⭐️⭐️⭐️⭐️', callback_data=f'+rating_5_{profile_id}_{current_page}'),
                 InlineKeyboardButton(text='⭐️⭐️⭐️⭐️', callback_data=f'+rating_4_{profile_id}_{current_page}'))
    keyboard.row(InlineKeyboardButton(text='⭐️⭐️⭐️', callback_data=f'+rating_3_{profile_id}_{current_page}'),
                 InlineKeyboardButton(text='⭐️⭐️', callback_data=f'+rating_2_{profile_id}_{current_page}'),
                 InlineKeyboardButton(text='⭐️', callback_data=f'+rating_1_{profile_id}_{current_page}'))
    keyboard.row(InlineKeyboardButton(text='Вернуться', callback_data=f'getdelegate_{profile_id}_{current_page}'))
    return keyboard.as_markup()


def set_level_kb(profile_id, current_page):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text='Поставить 1 уровень', callback_data=f'+level_1_{profile_id}_{current_page}'))
    keyboard.row(
        InlineKeyboardButton(text='Поставить 2 уровень', callback_data=f'+level_2_{profile_id}_{current_page}'))
    keyboard.row(
        InlineKeyboardButton(text='Поставить 3 уровень', callback_data=f'+level_3_{profile_id}_{current_page}'))
    keyboard.row(InlineKeyboardButton(text='Вернуться', callback_data=f'getdelegate_{profile_id}_{current_page}'))
    return keyboard.as_markup()


def add_coins_kb(profile_id, current_page):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text='+50 🪙', callback_data=f'+coin_50_{profile_id}_{current_page}'))
    keyboard.row(InlineKeyboardButton(text='+100 🪙', callback_data=f'+coin_100_{profile_id}_{current_page}'))
    keyboard.row(InlineKeyboardButton(text='+500 🪙', callback_data=f'+coin_500_{profile_id}_{current_page}'))
    keyboard.row(InlineKeyboardButton(text='-50 🪙', callback_data=f'-coin_50_{profile_id}_{current_page}'))
    keyboard.row(InlineKeyboardButton(text='-100 🪙', callback_data=f'-coin_100_{profile_id}_{current_page}'))
    keyboard.row(InlineKeyboardButton(text='-500 🪙', callback_data=f'-coin_500_{profile_id}_{current_page}'))
    keyboard.adjust(3)
    keyboard.row(InlineKeyboardButton(text='Поставить свое количество',
                                      callback_data=f'coin_custom_{profile_id}_{current_page}'))
    keyboard.row(InlineKeyboardButton(text='Вернуться', callback_data=f'getdelegate_{profile_id}_{current_page}'))
    return keyboard.as_markup()


def choose_coin_kb(coins, profile_id, current_page):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text='Прибавить монеты', callback_data=f'+coin_{coins}_{profile_id}_{current_page}'))
    keyboard.row(InlineKeyboardButton(text='Отнять монеты', callback_data=f'-coin_{coins}_{profile_id}_{current_page}'))
    keyboard.row(InlineKeyboardButton(text='Отменить', callback_data=f'add_coin_{profile_id}_{current_page}'))
    return keyboard.as_markup()


def delete_delegate_kb(profile_id, current_page):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text='Удалить', callback_data=f'deleted_delegate_{profile_id}_{current_page}'))
    keyboard.row(InlineKeyboardButton(text='Вернуться', callback_data=f'getdelegate_{profile_id}_{current_page}'))
    return keyboard.as_markup()
