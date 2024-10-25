from aiogram import Router, F  # Импортируем необходимые модули из aiogram
from aiogram.types import Message, CallbackQuery  # Импортируем необходимые типы

from config import load_config, Config  # Импортируем функции для загрузки конфигурации
from keyboards.profile_kb import main_back  # Импортируем основную клавиатуру
from states.registration import Registration  # Импортируем состояния регистрации
from aiogram.fsm.context import FSMContext  # Импортируем контекст FSM для управления состояниями
from aiogram.filters import StateFilter  # Импортируем фильтр состояния

from database.users import create_user  # Импортируем функцию для создания пользователя
from filters.regular_expressions import RegularExpressionsFilter  # Импортируем фильтр регулярных выражений
from keyboards.registration_keyboard import choose_role_kb, select_organize_kb  # Импортируем клавиатуры для выбора роли

# Создаем экземпляр роутера
router = Router()


# Обработчик сообщения для ввода и проверки инициалов пользователя
@router.message(Registration.initials,
                RegularExpressionsFilter(pattern=r'^[А-ЯЁ][а-яё]+\s[А-ЯЁ]\.[А-ЯЁ]$')
                )
async def choose_initials(message: Message, state: FSMContext):
    config: Config = load_config()  # Загружаем конфигурацию
    admin_ids_list: list = config.tg_bot.admin_ids  # Получаем список администраторов
    await state.update_data(initials=message.text)  # Сохраняем инициалы в состоянии
    if message.chat.id in admin_ids_list:
        # Если пользователь является администратором, предлагаем выбрать роль организатора
        await message.answer("Теперь выберите вашу роль на мероприятии.", reply_markup=select_organize_kb())
    else:
        # Если пользователь не является администратором, предлагаем выбрать стандартную роль
        await message.answer("Теперь выберите вашу роль на мероприятии.", reply_markup=choose_role_kb())


# Обработчик callback для выбора роли пользователя
@router.callback_query(F.data.startswith("reg"))
async def choose_role(call: CallbackQuery, state: FSMContext):
    role = call.data.split("_")[-1]  # Извлекаем выбранную роль из данных callback
    await state.update_data(role=role)  # Сохраняем роль в состоянии
    await call.message.edit_text(f"Ваша роль: {role}", reply_markup=None)  # Обновляем сообщение с подтверждением роли
    user_data = await state.get_data()  # Получаем все данные из состояния
    await state.clear()  # Очищаем состояние

    # Формируем текст подтверждения регистрации
    text = (f"Вы выбрали:\nИнициалы: {user_data['initials']}\nUsername: @{call.message.chat.username}\n"
            f"Роль: {user_data['role']}\nСпасибо за регистрацию!")
    # Создаем нового пользователя в базе данных
    await create_user(initials=user_data['initials'], username=f"@{call.message.chat.username}",
                      role=user_data['role'], userid=str(call.message.chat.id))
    # Отправляем сообщение с подтверждением регистрации и клавиатурой
    await call.message.answer(text, reply_markup=main_back())


# Обработчик сообщения для ввода некорректных инициалов
@router.message(StateFilter("Registration:initials"))
async def initials_incorrectly(message: Message):
    # Отправляем сообщение о некорректном формате инициалов
    await message.answer("Вы ввели неправильно инициалы. Введите как по шаблону - Фамилия И.О")
