from aiogram import F, Router  # Импортируем необходимые модули из aiogram
from aiogram.fsm.context import FSMContext  # Импортируем FSMContext для управления состояниями
from aiogram.types import Message, CallbackQuery  # Импортируем необходимые типы

# Импортируем функции и клавиатуры из других модулей
from database.events import create_event, get_events, delete_event_applications
from database.users import get_user_role
from keyboards.event_signup_kb import confirm_event_kb, event_choose, back_events
from keyboards.profile_kb import main_back
from states.create_event import EventStates

# Создаем экземпляр роутера
router = Router()


# Обработчик callback для создания мероприятия
@router.callback_query(F.data == "create_event")
async def pulse_menu(call: CallbackQuery):
    events = await get_events()
    if events:
        text = "Выбери мероприятие из списка ниже:"
    else:
        text = "Пока что нет актуальных мероприятий."
    role = await get_user_role(str(call.message.chat.id))  # Асинхронно получаем роль пользователя
    # Отправляем сообщение с информацией о событии и клавиатурой
    await call.message.edit_text(text, reply_markup=event_choose(events, role))


# Обработчик callback для удаления мероприятия
@router.callback_query(F.data.startswith("delete_event_"))
async def create_event_handler(call: CallbackQuery, state: FSMContext):
    event_id = int(call.data.split("_")[-1])
    await delete_event_applications(event_id)
    await call.message.edit_text("Удалили мероприятие.", reply_markup=back_events())


# Обработчик callback для обновления мероприятия
@router.callback_query(F.data == "make_event")
async def create_event_handler(call: CallbackQuery, state: FSMContext):
    events = await get_events()
    if len(events) >= 15:
        await call.message.edit_text("Достигнуто максимальное количество мероприятий.", reply_markup=back_events())
    else:
        await call.message.edit_text("Напишите название мероприятия:")
        await state.set_state(EventStates.event_name)  # Устанавливаем состояние ожидания текста мероприятия


# Обработчик сообщения для получения текста мероприятия
@router.message(EventStates.event_name)
async def receive_event_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)  # Сохраняем текст мероприятия в состоянии
    # Устанавливаем состояние ожидания максимального количества участников
    await message.answer("Напишите текст мероприятия:")
    await state.set_state(EventStates.waiting_for_event_text)  # Устанавливаем состояние ожидания текста мероприятия


# Обработчик сообщения для получения текста мероприятия
@router.message(EventStates.waiting_for_event_text)
async def receive_event_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)  # Сохраняем текст мероприятия в состоянии
    # Устанавливаем состояние ожидания максимального количества участников
    await state.set_state(EventStates.waiting_for_max_participants)
    await message.answer("Введите максимальное количество участников:")


# Обработчик сообщения для получения максимального количества участников
@router.message(EventStates.waiting_for_max_participants)
async def receive_max_participants(message: Message, state: FSMContext):
    try:
        max_participants = int(message.text)  # Преобразуем ввод в целое число
        await state.update_data(
            max_participants=max_participants)  # Сохраняем максимальное количество участников в состоянии
        data = await state.get_data()
        preview_text = (f"Предпросмотр мероприятия:\n\n{data['text']}\n\nМаксимальное количество участников: "
                        f"{data['max_participants']}")
        await state.set_state(EventStates.preview)  # Устанавливаем состояние пред просмотра
        # Отправляем предпросмотр мероприятия с клавиатурой подтверждения
        await message.answer(preview_text, reply_markup=confirm_event_kb())
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число для максимального количества участников.")


# Обработчик callback для отправки мероприятия
@router.callback_query(F.data == 'send_event')
async def send_event_handler(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await create_event(data['name'], data['text'], data['max_participants'])  # Создаем мероприятие в базе данных
    await state.clear()  # Очищаем состояние
    await callback_query.message.edit_text("Мероприятие отправлено.",
                                           reply_markup=main_back())  # Отправляем сообщение об успешной отправке


# Обработчик callback для отправки мероприятия без ограничения участников
@router.callback_query(F.data == 'send_event_skip')
async def send_event_handler(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await create_event(data['name'], data['text'], 0)  # Создаем мероприятие в базе данных без ограничения участников
    await state.clear()  # Очищаем состояние
    await callback_query.message.edit_text("Мероприятие отправлено.",
                                           reply_markup=main_back())  # Отправляем сообщение об успешной отправке


# Обработчик callback для отмены создания мероприятия
@router.callback_query(F.data == 'cancel_event')
async def cancel_event_handler(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()  # Очищаем состояние
    await callback_query.message.edit_text("Создание мероприятия отменено.",
                                           reply_markup=main_back())  # Отправляем сообщение об отмене
