from aiogram import Router, F  # Импортируем необходимые модули из aiogram
from aiogram.types import CallbackQuery  # Импортируем необходимые типы
import logging  # Импортируем модуль для логирования

from database.programs import get_program  # Импортируем функцию для получения программы из базы данных
from keyboards.profile_kb import main_back  # Импортируем клавиатуру

# Создаем экземпляр роутера
router = Router()


# Обработчик callback для отображения программы мероприятия
@router.callback_query(F.data == 'programs')
async def program_menu(call: CallbackQuery):
    try:
        program_text = await get_program()  # Получаем текст программы из базы данных
        if program_text:
            text = f"📅 Программа мероприятия:\n{program_text}"
        else:
            text = "Пока что нет актуальной программы."
        await call.message.edit_text(text, reply_markup=main_back())  # Отправляем текст программы с клавиатурой
    except Exception as e:
        logging.error(f"Error fetching program: {e}")
        await call.message.edit_text("Произошла ошибка при получении программы мероприятия. Попробуйте позже.",
                                     reply_markup=main_back())
