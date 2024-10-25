from aiogram import Router, F  # Импортируем необходимые модули из aiogram
from aiogram.types import CallbackQuery  # Импортируем CallbackQuery для работы с callback

# Импортируем функции и клавиатуры из других модулей
from database.users import get_rating
from keyboards.profile_kb import main_back

# Создаем экземпляр роутера
router = Router()


# Обработчик callback для показа рейтинга делегатов
@router.callback_query(F.data == 'delegate_rating')
async def rating_menu(call: CallbackQuery):
    all_rating = await get_rating()  # Получаем рейтинг всех пользователей из базы данных

    # Сортируем делегатов по рейтингу в порядке убывания и берем топ 5
    sorted_delegates = sorted(all_rating, key=lambda x: x[0], reverse=True)[:5]

    # Формируем текст для показа рейтинга делегатов
    delegate_text = """
    🏆 <b>Рейтинг Делегатов</b> 🏆

🥇 {0}

🥈 {1}

🥉 {2}

🏅 {3}

🏅 {4}

<b>✨ Чтобы попасть в топ 5, нужно быть активным участником. 🚀</b>
    """.format(
        f"<b>{sorted_delegates[0][3]}</b> - <b>{sorted_delegates[0][0]}</b>⭐️" if len(
            sorted_delegates) > 0 else "<b>(Пока пусто)</b>",
        f"<b>{sorted_delegates[1][3]}</b> - <b>{sorted_delegates[1][0]}</b>⭐️" if len(
            sorted_delegates) > 1 else "<b>(Пока пусто)</b>",
        f"<b>{sorted_delegates[2][3]}</b> - <b>{sorted_delegates[2][0]}</b>⭐️" if len(
            sorted_delegates) > 2 else "<b>(Пока пусто)</b>",
        f"<b>{sorted_delegates[3][3]}</b> - <b>{sorted_delegates[3][0]}</b>⭐️" if len(
            sorted_delegates) > 3 else "<b>(Пока пусто)</b>",
        f"<b>{sorted_delegates[4][3]}</b> - <b>{sorted_delegates[4][0]}</b>⭐️" if len(
            sorted_delegates) > 4 else "<b>(Пока пусто)</b>"
    )
    # Редактируем текст сообщения и добавляем клавиатуру назад
    await call.message.edit_text(delegate_text, reply_markup=main_back())
