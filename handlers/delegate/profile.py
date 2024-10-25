from aiogram import Router, F  # Импортируем необходимые модули из aiogram
from aiogram.filters import StateFilter  # Импортируем фильтр для состояний
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton  # Импортируем нужные типы
from aiogram.utils.keyboard import InlineKeyboardBuilder  # Импортируем InlineKeyboardBuilder для создания клавиатур

# Импортируем функции из других модулей для работы с базой данных и клавиатурами
from database.users import (get_user, get_rating, get_goals, create_goal, delete_goal, update_username,
                            update_initials, get_user_inventory, db)
from filters.regular_expressions import RegularExpressionsFilter
from keyboards.profile_kb import menu_profile_kb, add_goal_kb, add_new_goal_kb, back_successful, delete_goal_kb, \
    profile_back, inventory_kb, InventoryItemCallback, InventoryPageCallback, generate_inventory_keyboard
from states.goal import GoalState
from aiogram.fsm.context import FSMContext

from states.profile import InitialsState

# Создаем экземпляр роутера
router = Router()


# Обработчик callback для меню профиля
@router.callback_query(F.data == 'profile')
async def profile_menu(call: CallbackQuery):
    profile_id = call.message.chat.id
    profile = await get_user(str(profile_id))  # Получаем данные профиля пользователя
    all_rating = await get_rating()  # Получаем рейтинг всех пользователей

    # Фильтруем и сортируем рейтинг по убыванию
    filtered_rating = sorted([i for i in all_rating if i[0] > 0], reverse=True)
    all_ranking = {item[1]: rank + 1 for rank, item in enumerate(filtered_rating)}  # Создаем словарь для ранжирования

    # Извлекаем данные профиля
    initials = profile[0]
    username = profile[2]
    level = profile[4]
    rating = profile[5]
    coin = profile[6]
    if profile_id in all_ranking:
        ranking = all_ranking[profile_id]
    else:
        ranking = 'еще не в топе'

    # Получаем цели пользователя
    goals_text = ""
    goals = await get_goals(str(call.message.chat.id))
    if goals:
        for goal_ in goals:
            goals_text += f"🔸<b> {goal_[0]}\n</b>"
    else:
        goals_text += "🔸 У вас пока нет целей\n"

    # Формируем текст профиля
    profile_info = f"""
📝 <b>Ваш профиль:</b>

🔹 {initials}
🔹 {username}

🎯 <b>Мои цели:</b>
{goals_text}
💰 <b>Состояние счета (Монет):</b> {coin}

📊 <b>Ваш текущий уровень:</b> {level}

⭐️ <b>Ваш рейтинг:</b> {rating}

🏆 <b>Ваше место в рейтинге:</b> {ranking}
    """

    await call.message.edit_text(profile_info, reply_markup=menu_profile_kb())  # Отправляем сообщение с профилем


# Обработчик callback для изменения имени пользователя
@router.callback_query(F.data == 'change_username')
async def goal_menu(call: CallbackQuery):
    username = "@" + call.message.chat.username
    await update_username(str(call.message.chat.id), username)  # Обновляем имя пользователя в базе данных

    text = f"Ваш username был изменен на {username}"
    await call.message.edit_text(text, reply_markup=profile_back())  # Отправляем сообщение о смене имени


# Обработчик callback для изменения инициалов пользователя
@router.callback_query(F.data == 'change_initials')
async def goal_menu(call: CallbackQuery, state: FSMContext):
    username = "@" + call.message.chat.username
    await update_username(str(call.message.chat.id), username)  # Обновляем имя пользователя в базе данных

    text = f"Введите ваши инициалы по шаблону - Фамилия И. О"
    await call.message.edit_text(text)  # Запрашиваем ввод инициалов
    await state.set_state(InitialsState.change_initials)  # Устанавливаем состояние ожидания ввода инициалов


# Обработчик сообщения для изменения инициалов пользователя
@router.message(InitialsState.change_initials,
                RegularExpressionsFilter(pattern=r'^[А-ЯЁ][а-яё]+\s[А-ЯЁ]\.\s[А-ЯЁ]$'))
async def choose_initials(message: Message, state: FSMContext):
    initials = message.text
    await update_initials(str(message.chat.id), initials)  # Обновляем инициалы в базе данных
    await state.clear()  # Очищаем состояние
    await message.answer(f"Инициалы изменены на {initials}.", reply_markup=profile_back())  # Подтверждаем изменение


# Обработчик сообщения для неверного ввода инициалов
@router.message(StateFilter("InitialsState:change_initials"))
async def initials_incorrectly(message: Message):
    await message.answer("Вы ввели неправильно инициалы. Введите как по шаблону, включая пробелы - Фамилия И.О")


# Обработчик callback для добавления цели
@router.callback_query(F.data == 'add_goal')
async def goal_menu(call: CallbackQuery, state: FSMContext):
    await state.clear()
    text = f"Вот ваши цели:\n"
    goals = await get_goals(str(call.message.chat.id))  # Получаем цели пользователя
    if goals:
        for goal_ in goals:
            text += f"- {goal_[0]}\n"
        goals = len(goals)
    else:
        goals = 0
        text += "У вас пока нет целей\n"
    text += "\nМаксимальное количество целей: 5"
    await call.message.edit_text(text, reply_markup=add_goal_kb(goals))  # Отправляем сообщение с целями


# Обработчик callback для удаления цели
@router.callback_query(F.data == 'delete_goal')
async def add_new_goal(call: CallbackQuery):
    goals = await get_goals(str(call.message.chat.id))  # Получаем цели пользователя
    await call.message.edit_text("Выберите цель, которую хотите удалить:", reply_markup=delete_goal_kb(goals))


# Обработчик callback для подтверждения удаления цели
@router.callback_query(F.data.startswith("forcedelete"))
async def add_new_goal(call: CallbackQuery):
    goal_text = call.data.split("_")[-1]
    await delete_goal(str(call.message.chat.id), goal_text)  # Удаляем цель из базы данных
    await call.message.edit_text("Цель успешно удалена.", reply_markup=back_successful())


# Обработчик callback для добавления новой цели
@router.callback_query(F.data == 'add_new_goal')
async def add_new_goal(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Введите вашу цель, которую вы хотите достигнуть.", reply_markup=None)
    await state.set_state(GoalState.waiting_for_message)  # Устанавливаем состояние ожидания ввода цели


# Обработчик сообщения для добавления новой цели
@router.message(GoalState.waiting_for_message)
async def goal_message(message: Message, state: FSMContext):
    goal = message.text
    await state.update_data(goal=goal)
    await message.answer(f"Вот ваша цель:\n- {goal}\n\nУверены что хотите ее добавить?", reply_markup=add_new_goal_kb())


# Обработчик callback для подтверждения создания новой цели
@router.callback_query(F.data == 'create_new_goal')
async def add_new_goal(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.clear()  # Очищаем состояние
    await create_goal(data['goal'], str(call.message.chat.id))  # Создаем новую цель в базе данных
    await call.message.edit_text("Цель успешно создана.", reply_markup=back_successful())


# Обработчик callback для открытия инвентаря
@router.callback_query(F.data == 'inventory')
async def inventory_menu(call: CallbackQuery):
    user_id = call.message.chat.id
    items = await get_user_inventory(str(user_id))  # Получаем инвентарь пользователя
    total_items = len(items)
    total_pages = total_items // 9 + (1 if total_items % 9 else 0)
    current_page_items = items[:9]

    text = ""
    if total_items <= 0:
        text += ("🔹 У вас пока пустой инвентарь."
                 "\n\n✨ Не переживайте! Это только начало вашего приключения! 🌟"
                 "\n\n🗺️ Эти предметы можно купить в магазине за монеты. 🛒💰"
                 "\n\n⚡ Зарабатывайте монеты и наполняйте свой инвентарь вещами!")
    else:
        text += "🔹 Ваш инвентарь:"
    keyboard = generate_inventory_keyboard(current_page_items, 1, total_pages)
    await call.message.edit_text(text, reply_markup=keyboard)


# Обработчик callback для пагинации инвентаря
@router.callback_query(InventoryPageCallback.filter())
async def paginate_inventory(call: CallbackQuery, callback_data: InventoryPageCallback):
    page = callback_data.page
    user_id = call.message.chat.id

    items = await get_user_inventory(str(user_id))  # Получаем инвентарь пользователя
    offset = (page - 1) * 9
    current_page_items = items[offset:offset + 9]
    total_items = len(items)
    total_pages = (total_items + 8) // 9

    keyboard = inventory_kb(current_page_items, page, total_pages)
    await call.message.edit_reply_markup(reply_markup=keyboard)


# Обработчик callback для отображения деталей предмета инвентаря
@router.callback_query(InventoryItemCallback.filter())
async def show_inventory_item_details(call: CallbackQuery, callback_data: InventoryItemCallback):
    item_id = callback_data.item_id  # Используем item_id
    user_id = call.message.chat.id
    async with db.connection.execute("SELECT item, description FROM inventory WHERE userid = ? AND item_id = ?",
                                     (user_id, item_id)) as cursor:  # Запрос с использованием item_id
        item = await cursor.fetchone()
    user = await get_user(str(user_id))
    text = f"🎒 <b>Инвентарь {user[0]}🎒\n{item[0]}\n{item[1]}</b> "
    keyboard = InlineKeyboardBuilder().button(text="Вернуться", callback_data="inventory").as_markup()
    await call.message.edit_text(text, reply_markup=keyboard)
