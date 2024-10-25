from aiogram import F, Router  # Импортируем необходимые модули из aiogram
from aiogram.fsm.context import FSMContext  # Импортируем FSMContext для управления состояниями
from aiogram.types import CallbackQuery, Message  # Импортируем необходимые типы

# Импортируем функции и клавиатуры из других модулей
from database.rating import add_stars, get_user_stars
from database.users import (
    get_user, get_rating, get_goals, set_user_rating, set_user_level,
    set_user_coins, get_user_coins, delete_delegate
)
from keyboards.interaction_kb import (
    delegate_interaction_kb, interactive_kb, add_rating_kb, main_profile_back,
    set_level_kb, add_coins_kb, choose_coin_kb, delete_delegate_kb
)
from keyboards.profile_kb import main_back
from states.coins import CoinsStates

# Создаем экземпляр роутера
router = Router()


# Обработчик callback для показа меню взаимодействия с делегатами
@router.callback_query(F.data.startswith('delegate_interaction'))
async def interaction_menu(call: CallbackQuery):
    page = call.data.split("/")[-1]
    try:
        page = int(page)
    except ValueError:
        page = 1
    delegates = await get_rating()
    interaction_text = "Выбери делегата."
    await call.message.edit_text(interaction_text, reply_markup=interactive_kb(page, delegates))


# Обработчик callback для отображения профиля делегата
@router.callback_query(F.data.startswith("getdelegate_"))
async def interaction_menu(call: CallbackQuery):
    _, profile_id, current_page = call.data.split("_")
    profile = await get_user(profile_id)

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

🔹 {initials}
🔹 {username}

🎯 Цели:
{goals_text}
💰 <b>Состояние счета (Монет):</b> {coin}

📊 <b>Уровень</b>: {level}

⭐️ <b>Рейтинг</b>: {rating}
        """

    await call.message.edit_text(profile_info, reply_markup=delegate_interaction_kb(profile_id, current_page))


# Обработчик callback для пагинации влево и вправо
@router.callback_query(F.data.startswith('left_'))
async def paginate_left(call: CallbackQuery):
    current_page = int(call.data.split('_')[1])
    delegates = await get_rating()
    await call.message.edit_reply_markup(reply_markup=interactive_kb(current_page, delegates))


@router.callback_query(F.data.startswith('right_'))
async def paginate_right(call: CallbackQuery):
    current_page = int(call.data.split('_')[1])
    delegates = await get_rating()
    await call.message.edit_reply_markup(reply_markup=interactive_kb(current_page, delegates))


# Функция для обновления баланса монет
def update_coin_balance(current_coins: int, operation: str, amount: int):
    if operation == "+":
        current_coins += amount
    elif operation == "-":
        current_coins -= amount
        if current_coins < 0:
            current_coins = 0
    else:
        raise ValueError("Операция может быть только + или -")
    return current_coins


# Обработчик callback для добавления рейтинга
@router.callback_query(F.data.startswith("add_rating_"))
async def add_rating(call: CallbackQuery):
    profile_id, current_page = call.data.split("_")[2], call.data.split("_")[3]
    text = "Здесь вы можете добавить ему рейтинг:\nКак работает рейтинг?\nОн работает от суммы его накопленных звезд."
    await call.message.edit_text(text, reply_markup=add_rating_kb(profile_id, current_page))


# Обработчик callback для установки звезд
@router.callback_query(F.data.startswith("+rating_"))
async def set_stars(call: CallbackQuery):
    _, star, profile_id, current_page = call.data.split("_")
    star = int(star)
    text = f"Успешно поставили ему {star}⭐️"
    await add_stars(star, int(profile_id))

    stars = await get_user_stars(int(profile_id))
    await set_user_rating(profile_id, sum(star[0] for star in stars))

    await call.message.edit_text(text, reply_markup=main_profile_back(profile_id, current_page))


# Обработчик callback для изменения уровня делегата
@router.callback_query(F.data.startswith("set_level_"))
async def level_menu(call: CallbackQuery):
    profile_id, current_page = call.data.split("_")[2], call.data.split("_")[3]
    text = "Здесь вы можете сменить уровень делегата."
    await call.message.edit_text(text, reply_markup=set_level_kb(profile_id, current_page))


# Обработчик callback для установки уровня
@router.callback_query(F.data.startswith("+level_"))
async def set_level(call: CallbackQuery):
    _, level, profile_id, current_page = call.data.split("_")
    level = int(level)
    text = f"Успешно поставили ему {level} уровень"

    await set_user_level(profile_id, level)

    await call.message.edit_text(text, reply_markup=main_profile_back(profile_id, current_page))


# Обработчик callback для изменения количества монет
@router.callback_query(F.data.startswith("add_coin_"))
async def add_coin_menu(call: CallbackQuery):
    profile_id, current_page = call.data.split("_")[2], call.data.split("_")[3]
    text = "Здесь вы можете добавить или отнять монеты."
    await call.message.edit_text(text, reply_markup=add_coins_kb(profile_id, current_page))


@router.callback_query(F.data.startswith('coin_custom_'))
async def set_custom_coin(call: CallbackQuery, state: FSMContext):
    _, profile_id, current_page = call.data.split('_')[-3:]
    await call.message.edit_text("Напишите сколько монет вы хотите поставить (Только целые числа):")
    await state.update_data(profile_id=profile_id, current_page=current_page)
    await state.set_state(CoinsStates.waiting_for_message)


@router.message(CoinsStates.waiting_for_message)
async def choose_coin(message: Message, state: FSMContext):
    coins = int(message.text)
    data = await state.get_data()
    profile_id = data.get('profile_id')
    current_page = data.get('current_page')
    await state.clear()
    text = f"Теперь выберите операцию, что делать с {coins} 🪙"
    await message.answer(text, reply_markup=choose_coin_kb(coins, profile_id, current_page))


@router.callback_query(F.data.startswith("+coin_"))
async def add_coin(call: CallbackQuery):
    profile_id, coin, current_page = call.data.split("_")[2], call.data.split("_")[1], call.data.split("_")[-1]
    coin = int(coin)
    if coin == 1:
        text = f"Успешно отправили {coin} монету"
    else:
        text = f"Успешно отправили {coin} монет"

    current_coins = await get_user_coins(profile_id)
    await set_user_coins(profile_id, update_coin_balance(current_coins, call.data[0], coin))

    await call.message.edit_text(text, reply_markup=main_profile_back(profile_id, current_page))


@router.callback_query(F.data.startswith("-coin_"))
async def remove_coin(call: CallbackQuery):
    profile_id, coin, current_page = call.data.split("_")[2], call.data.split("_")[1], call.data.split("_")[-1]
    coin = int(coin)
    if coin == 1:
        text = f"Успешно отобрали {coin} монету"
    else:
        text = f"Успешно отобрали {coin} монет"

    current_coins = await get_user_coins(profile_id)
    await set_user_coins(profile_id, update_coin_balance(current_coins, call.data[0], coin))

    await call.message.edit_text(text, reply_markup=main_profile_back(profile_id, current_page))


# Обработчик callback для удаления делегата
@router.callback_query(F.data.startswith("remove_delegate_"))
async def remove_delegate(call: CallbackQuery):
    profile_id, current_page = call.data.split("_")[2], call.data.split("_")[3]
    text = "Вы уверены что хотите удалить делегата?"
    await call.message.edit_text(text, reply_markup=delete_delegate_kb(profile_id, current_page))


# Обработчик callback для подтверждения удаления делегата
@router.callback_query(F.data.startswith("deleted_delegate_"))
async def deleted_delegate(call: CallbackQuery):
    profile_id = call.data.split("_")[2]
    text = "Делегат был удален."
    await delete_delegate(profile_id)
    await call.message.edit_text(text, reply_markup=main_back())
