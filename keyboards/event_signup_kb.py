from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


def event_signup(role, amount, event_id):
    keyboard = InlineKeyboardBuilder()
    if role == "Делегат" and amount > 0:
        keyboard.row(InlineKeyboardButton(text='Записаться на мероприятие', callback_data=f'signup_event_{event_id}'))
        keyboard.row(InlineKeyboardButton(text='Вернуться', callback_data='pulse'))
    elif role == "Организатор":
        keyboard.row(InlineKeyboardButton(text='Удалить мероприятие', callback_data=f'delete_event_{event_id}'))
        keyboard.row(InlineKeyboardButton(text='Вернуться', callback_data='create_event'))
    else:
        keyboard.row(InlineKeyboardButton(text='Вернуться', callback_data='pulse'))
    return keyboard.as_markup()


def back_events():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text='Вернуться', callback_data='create_event'))
    return keyboard.as_markup()


def event_choose(events, role):
    keyboard = InlineKeyboardBuilder()
    for event in events:
        keyboard.button(text=f'{event[1]}', callback_data=f'event_{event[0]}')
    keyboard.adjust(3, repeat=True)
    if role == "Организатор" and len(events) < 15:
        keyboard.row(InlineKeyboardButton(text="Добавить мероприятие", callback_data="make_event"))
    keyboard.row(InlineKeyboardButton(text='Вернуться', callback_data='back_menu'))
    return keyboard.as_markup()


def confirm_event_kb():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text='Отправить с записью делегатов', callback_data='send_event'))
    keyboard.row(InlineKeyboardButton(text='Отправить без записи делегатов', callback_data='send_event_skip'))
    keyboard.row(InlineKeyboardButton(text='Отменить', callback_data='cancel_event'))
    return keyboard.as_markup()


def generate_delegates(page: int, page_size: int = 9, delegates: list = None):
    start = (page - 1) * page_size
    end = start + page_size
    return delegates[start:end]


def applications_kb(page: int, delegates: list, data: str = None):
    keyboard = InlineKeyboardBuilder()
    current_delegates = generate_delegates(page, delegates=delegates)
    for delegate in current_delegates:
        keyboard.row(
            InlineKeyboardButton(text=delegate[2], callback_data=f'application_{delegate[0]}_{page}')
        )
    keyboard.adjust(3)

    # Navigation buttons
    if page * 9 < len(delegates) and page > 1:
        keyboard.row(
            InlineKeyboardButton(text="<-", callback_data=f'app_left_{page - 1}'),
            InlineKeyboardButton(text="->", callback_data=f'app_right_{page + 1}'),
        )
    elif page > 1:
        keyboard.row(
            InlineKeyboardButton(text="<-", callback_data=f'app_left_{page - 1}'),
        )
    elif page * 9 < len(delegates):
        keyboard.row(
            InlineKeyboardButton(text="->", callback_data=f'app_right_{page + 1}'),
        )
    if data == "check_application":
        keyboard.row(
            InlineKeyboardButton(text='Принятые заявки', callback_data='added_applications')
        )
    keyboard.row(
        InlineKeyboardButton(text='Вернуться', callback_data='back_menu')
    )
    return keyboard.as_markup()


def application_mailing_kb():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text='Проверить', callback_data='check_application'))
    return keyboard.as_markup()


def application_delegate_kb():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text='Участник добавлен', callback_data='change_status_Добавлен'))
    keyboard.row(InlineKeyboardButton(text='Удалить из мероприятия', callback_data='delete_from_events'))
    keyboard.row(InlineKeyboardButton(text='Вернуться', callback_data='check_application'))
    return keyboard.as_markup()


def applications_back():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text='Вернуться', callback_data='check_application'))
    return keyboard.as_markup()


def menu_back():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text='Принятые заявки', callback_data='added_applications'))
    keyboard.row(InlineKeyboardButton(text='Вернуться', callback_data='back_menu'))
    return keyboard.as_markup()
