from aiogram import Router, types, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from database.users import create_user
from filters.regular_expressions import RegularExpressionsFilter
from keyboards.registration_keyboard import registration_keyboard, confirmation_keyboard

router = Router()

class Form(StatesGroup):
    initials = State()
    phone_number = State()


async def cancel_reg(message: types.Message, state: FSMContext, text) -> None:
    if message.text != None and message.text.strip().lower() == "отмена":
        await state.clear()
        await message.answer("Регистрация отменена.", reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer(text)


@router.message(Command("register"),)
async def cmd_register(message: types.Message, state: FSMContext):
    await message.answer("Введите ваши инициалы по шаблону - Фамилия И.О", reply_markup=registration_keyboard())
    await state.set_state(Form.initials)


@router.message(Form.initials,
                RegularExpressionsFilter(pattern=r'^[А-ЯЁ][а-яё]+\s[А-ЯЁ]\.\s[А-ЯЁ]$')
                )
async def send_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(initials=message.text)
    await message.answer("Нажмите на кнопку снизу, чтобы отправить нам номер телефона.", reply_markup=registration_keyboard(is_number=True))
    await state.set_state(Form.phone_number)


@router.message(Form.phone_number,
                F.contact)
async def phone_number_choosen(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    if not phone_number.startswith('+'):
        phone_number = f'+{phone_number}'

    user_data = await state.get_data()
    await state.update_data(phone=phone_number)
    await state.update_data(username=f"@{message.from_user.username}")
    await state.update_data(userid=message.from_user.id)

    text = f"Вы выбрали:\nИнициалы: {user_data['initials']}\nНомер телефона: {phone_number}\nUsername: @{message.from_user.username}\nВ случае если вы сменили Username, то в профиле бота смените его, иначе нам будет трудно связаться с вами."
    await message.answer(text, reply_markup=types.ReplyKeyboardRemove())
    await message.answer(f"Все правильно?", reply_markup=confirmation_keyboard())


@router.message(StateFilter("Form:initials"))
async def initials_incorrectly(message: types.Message, state: FSMContext):
    text = "Вы ввели неправильно инициалы. Введите как по шаблону, включая пробелы - Фамилия И.О (Иванов И.И)"
    await cancel_reg(message, state, text)


@router.message(StateFilter("Form:phone_number"))
async def phone_number_incorrectly(message: types.Message, state: FSMContext):
    text = "Нажмите на кнопку снизу, чтобы отправить нам номер телефона."
    await cancel_reg(message, state, text)


@router.callback_query(F.data == "confirm")
async def confirm_handler(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    await create_user(user_data['initials'], user_data['phone'], user_data['username'], user_data['userid'])
    await callback_query.message.edit_text("Регистрация завершена.", reply_markup=None)


@router.callback_query(F.data == "cancel_registration")
async def edit_phone_number_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text("Регистрация отменена.", reply_markup=None)