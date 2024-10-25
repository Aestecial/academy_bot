from aiogram import Router, F  # Импортируем необходимые модули из aiogram
from aiogram.types import CallbackQuery  # Импортируем CallbackQuery для работы с callback

from database.users import deleted_user
# Импортируем функции и клавиатуры из других модулей
from keyboards.delete_guest_kb import delete_guest_kb
from keyboards.profile_kb import main_back

# Создаем экземпляр роутера
router = Router()


# Обработчик callback для показа рейтинга делегатов
@router.callback_query(F.data == 'delete_yourself')
async def guest_delete(call: CallbackQuery):
    text = "Вы точно хотите удалить себя?"
    await call.message.edit_text(text, reply_markup=delete_guest_kb())


@router.callback_query(F.data == 'deleted_guest')
async def guest_delete(call: CallbackQuery):
    text = "Пользователь был удален."
    await deleted_user(str(call.message.chat.id))
    await call.message.edit_text(text, reply_markup=main_back())
