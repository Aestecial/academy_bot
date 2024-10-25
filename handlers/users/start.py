from aiogram import Router, F  # Импортируем необходимые классы и функции из библиотеки aiogram
from aiogram.types import Message, \
    CallbackQuery  # Импортируем классы Message и CallbackQuery для работы с сообщениями и обратными вызовами
from aiogram.filters import CommandStart  # Импортируем фильтр CommandStart для обработки команды /start

from states.registration import Registration  # Импортируем состояние регистрации из соответствующего модуля
from aiogram.fsm.context import FSMContext  # Импортируем контекст машины состояний (FSMContext)

from database.users import get_user_role  # Импортируем функцию для получения роли пользователя из базы данных
from keyboards.start_keyboard import start_kb  # Импортируем клавиатуру для начального меню

# Создаем экземпляр роутера, который будет обрабатывать входящие сообщения и обратные вызовы
router = Router()

# Определяем приветственные сообщения для различных ролей пользователей
greetings = {
    "Организатор": "👋 <b>Приветствую, организатор!</b>"
                   "\n🔹 Я ваш помощник, готовый помочь вам на каждом этапе подготовки и проведения мероприятия. 💪",
    "Делегат": "👋 <b>Приветствую, делегат!</b>"
               "\n🔹 Я ваш помощник, готовый помочь вам на каждом этапе вашего участия. 💪",
    "Гость": "👋 <b>Приветствую, уважаемый гость! </b>"
             "\n🔹 Я ваш помощник, готовый сделать ваше пребывание здесь максимально комфортным и информативным. 💪",
}


# Обработчик команды /start
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    # Получаем роль пользователя по его ID
    role = await get_user_role(str(message.chat.id))
    if role:
        # Если роль пользователя найдена, отправляем соответствующее приветственное сообщение и клавиатуру
        await message.answer(greetings[role], reply_markup=start_kb(role))
    else:
        # Если роль пользователя не найдена, переводим пользователя в состояние ввода инициалов и отправляем инструкцию
        await state.set_state(Registration.initials)
        await message.answer("👋 Привет!\n\n"
                             "✨ Я бот для регистрации на мероприятие. ✨\n\n"
                             "🔹 Пожалуйста, введите ваши инициалы по шаблону:\n\n"
                             "Фамилия И.О\n\n"
                             "💡 Например: Иванов И.И")


# Обработчик обратного вызова для возврата в начальное меню
@router.callback_query(F.data == "back_menu")
async def cmd_start_query(call: CallbackQuery, state: FSMContext):
    # Получаем роль пользователя по его ID
    role = await get_user_role(str(call.message.chat.id))
    if role:
        # Если роль пользователя найдена, редактируем сообщение с соответствующим приветствием и клавиатурой
        await call.message.edit_text(greetings[role], reply_markup=start_kb(role))
    else:
        # Если роль пользователя не найдена, переводим пользователя
        # в состояние ввода инициалов и редактируем сообщение с инструкцией
        await state.set_state(Registration.initials)
        await call.message.edit_text("👋 Привет!\n\n"
                                     "✨ Я бот для регистрации на мероприятие. ✨\n\n"
                                     "🔹 Пожалуйста, введите ваши инициалы по шаблону:\n\n"
                                     "Фамилия И.О\n\n"
                                     "💡 Например: Иванов И.И")
