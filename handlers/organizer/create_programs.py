from aiogram import F, Router  # Импортируем необходимые модули из aiogram
from aiogram.fsm.context import FSMContext  # Импортируем FSMContext для управления состояниями
from aiogram.types import Message, CallbackQuery  # Импортируем необходимые типы

# Импортируем функции и клавиатуры из других модулей
from database.programs import get_program, create_program
from keyboards.profile_kb import main_back
from keyboards.programs_kb import programs_kb, preview_kb

from states.create_programs import ProgramsStates  # Импортируем состояния для создания программы

# Создаем экземпляр роутера
router = Router()


# Обработчик callback для показа программы мероприятия
@router.callback_query(F.data == "create_programs")
async def create_programs_menu(call: CallbackQuery):
    program_text = await get_program()  # Получаем текст программы из базы данных
    text = f"📅 Программа мероприятия:\n{program_text}"
    await call.message.edit_text(text, reply_markup=programs_kb())  # Отправляем текст программы с клавиатурой


# Обработчик callback для обновления программы мероприятия
@router.callback_query(F.data == "update_programs")
async def create_programs_handler(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Пожалуйста, напишите текст программы:")
    await state.set_state(ProgramsStates.waiting_for_event_text)  # Устанавливаем состояние ожидания текста программы


# Обработчик сообщения для получения текста программы
@router.message(ProgramsStates.waiting_for_event_text)
async def receive_programs_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)  # Сохраняем текст программы в состоянии
    data = await state.get_data()  # Получаем все данные состояния
    preview_text = f"Предпросмотр программы:\n{data['text']}"
    await message.answer(preview_text,
                         reply_markup=preview_kb())  # Отправляем предпросмотр программы с клавиатурой подтверждения


# Обработчик callback для отправки программы
@router.callback_query(F.data == 'send_programs')
async def send_programs_handler(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()  # Получаем все данные состояния
    await create_program(data['text'])  # Сохраняем программу в базе данных
    await callback_query.message.edit_text("Программа отправлена.",
                                           reply_markup=main_back())  # Отправляем сообщение об успешной отправке
    data = dict()  # Очищаем глобальную переменную


# Обработчик callback для отмены создания программы
@router.callback_query(F.data == 'cancel_programs')
async def cancel_programs_handler(callback_query: CallbackQuery):
    await callback_query.message.edit_text("Создание программы отменено.",
                                           reply_markup=main_back())  # Отправляем сообщение об отмене
