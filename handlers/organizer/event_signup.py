from aiogram import F, Router, Bot  # Импортируем необходимые модули из aiogram
from aiogram.fsm.context import FSMContext  # Импортируем FSMContext для управления состояниями
from aiogram.types import CallbackQuery  # Импортируем необходимые типы

# Импортируем функции и клавиатуры из других модулей
from database.event_applications import (
    get_user_application, create_application, get_all_organizers,
    get_users_application, remove_user_application, set_application_status,
    get_all_applications
)
from database.events import get_events, get_event
from database.users import get_user, get_goals
from keyboards.event_signup_kb import (
    application_mailing_kb, applications_kb, application_delegate_kb,
    applications_back, menu_back
)
from keyboards.profile_kb import main_back

# Создаем экземпляр роутера
router = Router()


# Обработчик callback для записи на мероприятие
@router.callback_query(F.data.startswith('signup_event_'))
async def event_signup(call: CallbackQuery, bot: Bot, state: FSMContext):
    event_id = int(call.data.split("_")[-1])
    profile_id = str(call.message.chat.id)
    event = await get_event(event_id)
    await state.update_data(profile_id=profile_id)

    user_application = await get_user_application(profile_id)
    all_applications = await get_all_applications()

    if user_application:
        text = "Вы уже записаны на мероприятие."
    elif len(all_applications) >= event[-1]:
        text = "Максимальное количество записей достигло лимита."
    else:
        text = "Успешно записались на мероприятие."
        user = await get_user(profile_id)
        await create_application(user[0], user[2], user[3], event_id)

        organizers = await get_all_organizers()
        for organizer in organizers:
            or_text = "Появилась новая запись на мероприятие."
            await bot.send_message(organizer[0], or_text, reply_markup=application_mailing_kb())

    await call.message.edit_text(text, reply_markup=main_back())


# Обработчик callback для проверки заявок на мероприятие
@router.callback_query(F.data.startswith('check_application'))
async def check_application(call: CallbackQuery, state: FSMContext):
    page = call.data.split("/")[-1]
    try:
        page = int(page)
    except ValueError:
        page = 1

    delegates = await get_users_application('Новый')
    await state.update_data(delegates=delegates, current_page=page)

    if delegates:
        text = "Выбери делегата."
        await call.message.edit_text(text, reply_markup=applications_kb(page, delegates, call.data))
    else:
        text = "Новых заявок пока нет."
        await call.message.edit_text(text, reply_markup=menu_back())


# Обработчик callback для пагинации влево
@router.callback_query(F.data.startswith('app_left_'))
async def paginate_left(call: CallbackQuery, state: FSMContext):
    page = int(call.data.split('_')[2])
    data = await state.get_data()
    delegates = data.get('delegates')
    await state.update_data(current_page=page)

    if page == 1:
        await call.message.edit_reply_markup(reply_markup=applications_kb(page, delegates, "check_application"))
    else:
        await call.message.edit_reply_markup(reply_markup=applications_kb(page, delegates))


# Обработчик callback для пагинации вправо
@router.callback_query(F.data.startswith('app_right_'))
async def paginate_right(call: CallbackQuery, state: FSMContext):
    page = int(call.data.split('_')[2])
    data = await state.get_data()
    delegates = data.get('delegates')
    await state.update_data(current_page=page)

    await call.message.edit_reply_markup(reply_markup=applications_kb(page, delegates))


# Обработчик callback для проверки делегата
@router.callback_query(F.data.startswith('application_'))
async def check_delegate(call: CallbackQuery, state: FSMContext):
    _, profile_id, current_page = call.data.split("_")
    profile = await get_user(profile_id)

    user_app = await get_user_application(profile_id)
    event_id = user_app[-1]
    event = await get_event(event_id)
    event_name = event[1]

    initials = profile[0]
    username = profile[2]
    level = profile[4]
    rating = profile[5]
    coin = profile[6]

    goals_text = ""
    goals = await get_goals(profile_id)
    if goals:
        for goal_ in goals:
            goals_text += f"🔸<b> {goal_[0]}\n</b>"
    else:
        goals_text += "🔸 У вас пока нет целей\n"

    profile_info = f"""
📝 <b>Профиль делегата</b>:

🎟 <b>Мероприятие</b>: {event_name}

🔹 {initials}
🔹 {username}

🎯 Цели:
{goals_text}
💰 <b>Состояние счета (Монет):</b> {coin}

📊 <b>Уровень</b>: {level}

⭐️ <b>Рейтинг</b>: {rating}
"""
    await state.update_data(profile_id=profile_id, current_page=current_page)
    await call.message.edit_text(profile_info, reply_markup=application_delegate_kb())


# Обработчик callback для удаления делегата из мероприятия
@router.callback_query(F.data == 'delete_from_events')
async def delete_from_events(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    profile_id = data.get('profile_id')
    await remove_user_application(profile_id)
    await call.message.edit_text("Делегат был удален из мероприятия.", reply_markup=applications_back())


# Обработчик callback для изменения статуса заявки
@router.callback_query(F.data.startswith('change_status_'))
async def status_change(call: CallbackQuery, state: FSMContext):
    status = call.data.split("_")[-1]
    data = await state.get_data()
    profile_id = data.get('profile_id')
    await set_application_status(profile_id, status)
    await call.message.edit_text("Статус был изменен.", reply_markup=applications_back())


# Обработчик callback для проверки добавленных заявок на мероприятие
@router.callback_query(F.data.startswith('added_applications'))
async def check_added_application(call: CallbackQuery, state: FSMContext):
    page = call.data.split("/")[-1]
    try:
        page = int(page)
    except ValueError:
        page = 1

    delegates = await get_users_application('Добавлен')
    await state.update_data(delegates=delegates, current_page=page)

    if delegates:
        text = "Выбери делегата."
        await call.message.edit_text(text, reply_markup=applications_kb(page, delegates))
    else:
        text = "Новых принятых заявок пока нет."
        await call.message.edit_text(text, reply_markup=applications_back())
