from aiogram import Router, F, Bot  # Импортируем необходимые модули из aiogram
from aiogram.fsm.context import FSMContext  # Импортируем FSMContext для управления состояниями
from aiogram.types import CallbackQuery, Message  # Импортируем необходимые типы

# Импортируем функции и клавиатуры из других модулей
from database.event_applications import get_all_organizers
from database.users import get_user
from keyboards.profile_kb import main_back
from keyboards.write_organizer_kb import write_organizer_kb
from states.write_organizer import WriteStates

# Создаем экземпляр роутера
router = Router()


# Обработчик callback для начала написания сообщения организаторам
@router.callback_query(F.data == 'write_organizer')
async def write_organizer_menu(call: CallbackQuery, state: FSMContext):
    text = "Напишите сообщение, которое увидят все организаторы:"
    await call.message.edit_text(text, reply_markup=None)
    await state.set_state(WriteStates.waiting_for_message)  # Устанавливаем состояние ожидания ввода сообщения


# Обработчик сообщения для проверки текста сообщения
@router.message(WriteStates.waiting_for_message)
async def check_message(message: Message, state: FSMContext):
    organizer_text = message.text
    user = await get_user(str(message.chat.id))
    text = "Вот так будет выглядеть сообщение:\n"
    text += (f"✉️ <b>НОВОЕ СООБЩЕНИЕ</b> ✉️\n<b>Сообщение:</b>\n💬 {organizer_text}"
             f"\n<b>От пользователя:</b>\n👤 {user[0]} ({user[2]})")
    await state.update_data(organizer_text=organizer_text)  # Сохраняем текст сообщения в состоянии
    await message.answer(text, reply_markup=write_organizer_kb())  # Отправляем сообщение с клавиатурой подтверждения


# Обработчик callback для отправки сообщения организаторам
@router.callback_query(F.data == 'send_organizers')
async def send_organizers(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()  # Получаем данные состояния
    organizer_text = data.get('organizer_text')
    text = "Сообщение успешно отправлено."
    user = await get_user(str(call.message.chat.id))  # Получаем данные пользователя
    send_text = (f"✉️ <b>НОВОЕ СООБЩЕНИЕ</b> ✉️\n<b>Сообщение:</b>\n💬 {organizer_text}"
                 f"\n<b>От пользователя:</b>\n👤 {user[0]} ({user[2]})")
    organizers = await get_all_organizers()  # Получаем список всех организаторов
    await state.clear()  # Очищаем состояние
    await call.message.edit_text(text, reply_markup=main_back())  # Отправляем сообщение об успешной отправке
    for organizer in organizers:
        await bot.send_message(organizer[0], send_text)  # Отправляем сообщение каждому организатору


# Обработчик callback для отмены написания сообщения организаторам
@router.callback_query(F.data == 'cancel_write_organizer')
async def cancel_mailing(call: CallbackQuery, state: FSMContext):
    await state.clear()  # Очищаем состояние
    await call.message.edit_text("Сообщение организаторам отменено.",
                                 reply_markup=main_back())  # Отправляем сообщение об отмене
