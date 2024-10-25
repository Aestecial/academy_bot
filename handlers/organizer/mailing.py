from aiogram import Bot, F, Router  # Импортируем необходимые модули из aiogram
from aiogram.fsm.context import FSMContext  # Импортируем FSMContext для управления состояниями
from aiogram.types import CallbackQuery, Message  # Импортируем необходимые типы
from database.users import (
    get_user_mailing, get_all_user_mailing, get_user_mailing_without_level
)  # Импортируем функции для работы с базой данных
from keyboards.mailing_kb import mailing_kb, redact_kb, delegate_level  # Импортируем клавиатуры
from states.mailing import MailingState  # Импортируем состояния для управления процессом рассылки
from keyboards.profile_kb import main_back  # Импортируем основную клавиатуру

# Создаем экземпляр роутера
router = Router()


# Обработчик callback для начала создания рассылки
@router.callback_query(F.data == "create_mailing")
async def handle_mailing(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text("Введите сообщение для рассылки:")
    await state.set_state(MailingState.waiting_for_message)  # Устанавливаем состояние ожидания сообщения


# Обработчик сообщения для получения текста рассылки
@router.message(MailingState.waiting_for_message)
async def mailing_choose(message: Message, state: FSMContext):
    await state.update_data(text=message.text)  # Сохраняем текст сообщения в состоянии
    await message.answer("Теперь выберите кому вы хотите это отправить.", reply_markup=mailing_kb())


# Обработчик callback для выбора уровня делегатов
@router.callback_query(F.data == 'mailing_Делегат')
async def mailing_level(call: CallbackQuery, state: FSMContext):
    await state.update_data(role="Делегат")
    await call.message.edit_text("Введите уровень делегата:", reply_markup=delegate_level())


# Обработчик callback для подтверждения уровня делегатов
@router.callback_query(F.data.startswith("delegate/"))
async def mailing_choose(call: CallbackQuery, state: FSMContext):
    level = call.data.split("/")[-1]
    await state.update_data(level=level)
    user_data = await state.get_data()

    text = f"Вот так будет выглядеть рассылка:\n\n🔔 <b>РАССЫЛКА</b> 🔔\n{user_data['text']}"
    text += f"\n\nРассылка будет отправлена:\nРоль: {user_data['role']}\nУровень: {user_data['level']}"

    await call.message.edit_text(text, reply_markup=redact_kb())


# Обработчик callback для выбора роли
@router.callback_query(F.data.startswith('mailing_'))
async def mailing_role(call: CallbackQuery, state: FSMContext):
    role = call.data.split("_")[-1]
    await state.update_data(role=role)
    await state.update_data(level="Все")
    user_data = await state.get_data()
    text = f"Вот так будет выглядеть рассылка:\n\n🔔 <b>РАССЫЛКА</b> 🔔\n{user_data['text']}"
    text += f"\n\nРассылка будет отправлена:\nРоль: {user_data['role']}"

    await call.message.edit_text(text, reply_markup=redact_kb())


# Обработчик callback для начала рассылки
@router.callback_query(F.data == 'start_mailing')
async def start_mailing(call: CallbackQuery, state: FSMContext, bot: Bot):
    user_data = await state.get_data()
    if user_data['role'] == 'Все':
        users = await get_all_user_mailing()
    elif user_data['role'] == 'Делегат' and user_data['level'] != "Всем":
        users = await get_user_mailing(user_data['role'], int(user_data['level']))
    else:
        users = await get_user_mailing_without_level(user_data['role'])

    for user in users:
        text = f"🔔 <b>РАССЫЛКА</b> 🔔\n{user_data['text']}"
        await bot.send_message(chat_id=int(user[0]), text=text)

    await call.message.edit_text("Рассылка успешно отправлена.", reply_markup=main_back())


# Обработчик callback для редактирования рассылки
@router.callback_query(F.data == 'redact_mailing')
async def redact_mailing(call: CallbackQuery):
    await call.message.edit_text("Теперь выберите кому вы хотите это отправить.", reply_markup=mailing_kb())


# Обработчик callback для отмены рассылки
@router.callback_query(F.data == 'cancel_mailing')
async def cancel_mailing(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text("Рассылка отменена.", reply_markup=main_back())
