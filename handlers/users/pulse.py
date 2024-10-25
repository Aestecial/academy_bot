from aiogram import Router, F  # Импортируем необходимые модули из aiogram
from aiogram.types import CallbackQuery  # Импортируем тип CallbackQuery из aiogram

from database.users import get_user_role  # Импортируем функцию для получения роли пользователя из базы данных
from database.events import get_events, get_event  # Импортируем функцию для получения событий из базы данных
from keyboards.event_signup_kb import \
    event_signup, event_choose  # Импортируем функцию для создания клавиатуры для записи на мероприятие

# Создаем экземпляр роутера
router = Router()


# Обработчик callback для отображения актуального события
@router.callback_query(F.data == 'pulse')
async def pulse_menu(call: CallbackQuery):
    events = await get_events()
    if events:
        text = "Выбери мероприятие из списка ниже:"
    else:
        text = "Пока что нет актуальных мероприятий."
    role = await get_user_role(str(call.message.chat.id))  # Асинхронно получаем роль пользователя
    # Отправляем сообщение с информацией о событии и клавиатурой
    await call.message.edit_text(text, reply_markup=event_choose(events, role))


# Обработчик callback для отображения актуального события
@router.callback_query(F.data.startswith('event_'))
async def event_menu(call: CallbackQuery):
    event_id = int(call.data.split("_")[-1])
    event = await get_event(event_id)  # Асинхронно получаем текущее событие из базы данных
    text = f"🌟 <b>{event[1]}</b>\n{event[2]}"  # Формируем начальный текст с информацией о событии
    # Добавляем информацию о максимальном количестве участников, если это число больше нуля
    if event[-1] > 0:
        text += f"\nМаксимум участников: {event[-1]}"
    role = await get_user_role(str(call.message.chat.id))  # Асинхронно получаем роль пользователя
    # Отправляем сообщение с информацией о событии и клавиатурой
    await call.message.edit_text(text, reply_markup=event_signup(role, event[-1], event_id))
