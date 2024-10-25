from aiogram import Router, F  # Импортируем необходимые модули из aiogram
from aiogram.fsm.context import FSMContext  # Импортируем FSMContext для управления состояниями
from aiogram.types import CallbackQuery, Message  # Импортируем необходимые типы

# Импортируем функции из других модулей для работы с базой данных и клавиатурами
from database.users import get_item_inventory
from keyboards.profile_kb import main_back
from database.base import DataBase
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.shop_kb import ItemCallback, generate_shop_keyboard, PageCallback
from states.shop import AddItem, EditItem

# Создаем экземпляр роутера и базы данных
router = Router()
db = DataBase()


# Обработчик callback для открытия магазина
@router.callback_query(F.data == 'shop')
async def shop_menu(call: CallbackQuery):
    await db.connect()  # Подключаемся к базе данных
    items = await db.fetch_items()  # Получаем товары из базы данных
    total_items = await db.count_items()  # Получаем общее количество товаров
    total_pages = total_items // 9 + (1 if total_items % 9 else 0)  # Вычисляем количество страниц

    role = await db.get_user_role(call.message.chat.id)  # Получаем роль пользователя
    is_organizer = role == "Организатор"
    text = "✨ Добро пожаловать в наш магазин! ✨"
    keyboard = generate_shop_keyboard(items, 1, total_pages, is_organizer)  # Генерируем клавиатуру магазина

    await call.message.edit_text(text, reply_markup=keyboard)  # Отправляем сообщение с клавиатурой


# Обработчик callback для добавления товара
@router.callback_query(F.data == 'add_item')
async def add_item_start(call: CallbackQuery, state: FSMContext):
    role = await db.get_user_role(call.from_user.id)  # Получаем роль пользователя
    if role != "Организатор":
        await call.message.answer("Только организаторы могут добавлять предметы.")  # Проверяем роль пользователя
        return

    await state.set_state(AddItem.waiting_for_name)  # Устанавливаем состояние ожидания ввода имени товара
    await call.message.edit_text("Введите название предмета:", reply_markup=None)


# Обработчик сообщения для получения имени товара
@router.message(AddItem.waiting_for_name)
async def item_id_received(message: Message, state: FSMContext):
    await state.update_data(name=message.text)  # Обновляем данные состояния
    await state.set_state(AddItem.waiting_for_description)  # Устанавливаем состояние ожидания ввода описания
    await message.answer("Введите описание предмета:")


# Обработчик сообщения для получения описания товара
@router.message(AddItem.waiting_for_description)
async def item_description_received(message: Message, state: FSMContext):
    await state.update_data(description=message.text)  # Обновляем данные состояния
    await state.set_state(AddItem.waiting_for_price)  # Устанавливаем состояние ожидания ввода цены
    await message.answer("Введите цену предмета:")


# Обработчик сообщения для получения цены товара
@router.message(AddItem.waiting_for_price)
async def item_price_received(message: Message, state: FSMContext):
    await state.update_data(price=message.text)  # Обновляем данные состояния
    await state.set_state(AddItem.waiting_for_amount)  # Устанавливаем состояние ожидания ввода количества
    await message.answer("Введите количество предмета:")


# Обработчик сообщения для получения количества товара
@router.message(AddItem.waiting_for_amount)
async def item_amount_received(message: Message, state: FSMContext):
    await state.update_data(amount=message.text)  # Обновляем данные состояния

    data = await state.get_data()  # Получаем все данные состояния
    # Выполняем вставку нового товара в базу данных
    await db.connection.execute(
        "INSERT INTO shop (name, description, price, amount) VALUES (?, ?, ?, ?)",
        (data['name'], data['description'], data['price'], data['amount'])
    )
    await db.connection.commit()  # Подтверждаем изменения в базе данных

    await state.clear()  # Очищаем состояние
    await message.answer("Предмет успешно добавлен в магазин!", reply_markup=main_back())


# Обработчик callback для пагинации товаров
@router.callback_query(PageCallback.filter())
async def paginate(call: CallbackQuery, callback_data: PageCallback):
    page = callback_data.page  # Получаем номер страницы

    offset = (page - 1) * 9  # Вычисляем смещение для выборки товаров

    items = await db.fetch_items(offset=offset)  # Получаем товары с учетом смещения
    total_items = await db.count_items()  # Получаем общее количество товаров
    total_pages = (total_items + 8) // 9  # Вычисляем количество страниц
    role = await db.get_user_role(call.message.chat.id)  # Получаем роль пользователя
    is_organizer = role == "Организатор"

    current_page_items = items[:9]  # Получаем товары для текущей страницы
    if not current_page_items and page > 1:
        page -= 1
        offset = (page - 1) * 9
        items = await db.fetch_items(offset=offset)
        current_page_items = items[:9]

    keyboard = generate_shop_keyboard(current_page_items, page, total_pages, is_organizer)  # Генерируем клавиатуру
    await call.message.edit_reply_markup(reply_markup=keyboard)  # Обновляем клавиатуру сообщения


# Обработчик callback для просмотра деталей товара
@router.callback_query(ItemCallback.filter(F.action == "view"))
async def show_item_details(call: CallbackQuery, callback_data: ItemCallback):
    item_id = callback_data.item_id  # Получаем имя товара
    await db.connect()
    async with db.connection.execute("SELECT * FROM shop WHERE item_id = ?",
                                     (item_id,)) as cursor:
        item = await cursor.fetchone()

    # Проверка количества предметов, купленных пользователями
    async with db.connection.execute("SELECT COUNT(*) FROM inventory WHERE item = ?", (item[0],)) as cursor:
        count = await cursor.fetchone()
        sold_count = int(count[0])

    text = (f"<b>{item[0]}</b>"
            f"\n<b>{item[1]}</b>"
            f"\n\n💰 <b>Цена:</b> {item[2]} 🪙"
            f"\n📦 <b>Осталось:</b> {item[3] - sold_count} шт.")

    role = await db.get_user_role(call.from_user.id)
    if role == "Организатор":
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="Удалить предмет",
                        callback_data=ItemCallback(action="delete", item_id=str(item[-1])).pack())
        keyboard.button(text="Изменить количество",
                        callback_data=ItemCallback(action="edit_amount", item_id=str(item[-1])).pack())
        keyboard.button(text="Вернуться", callback_data="shop")
        keyboard.adjust(1, repeat=True)
        keyboard = keyboard.as_markup()
    elif item[3] - sold_count <= 0:
        text += "\n\n<b>🎉 Следите за обновлениями, чтобы не пропустить новые поступления! 🌟</b>"
        keyboard = InlineKeyboardBuilder().button(text="Вернуться", callback_data="shop").as_markup()
    else:
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="Купить", callback_data=ItemCallback(action="buy", item_id=str(item[-1])))
        keyboard.button(text="Вернуться", callback_data="shop")
        keyboard.adjust(1, repeat=True)
        keyboard = keyboard.as_markup()
    await call.message.edit_text(text, reply_markup=keyboard)


# Обработчик callback для покупки товара
@router.callback_query(ItemCallback.filter(F.action == "buy"))
async def buy_item(call: CallbackQuery, callback_data: ItemCallback):
    user_id = call.from_user.id
    item_id = callback_data.item_id
    async with db.connection.execute("SELECT amount, name FROM shop WHERE item_id = ?", (item_id,)) as cursor:
        amount = await cursor.fetchone()

    role = await db.get_user_role(user_id)

    buy_amount = len(await get_item_inventory(amount[-1]))

    if role == "Делегат" and buy_amount < amount[0]:
        async with db.connection.execute("SELECT name, description, price FROM shop WHERE item_id = ?",
                                         (item_id,)) as cursor:
            item = await cursor.fetchone()

        async with db.connection.execute("SELECT coins FROM users WHERE userid = ?", (user_id,)) as cursor:
            user = await cursor.fetchone()
            user_coins = int(user[0])

        async with db.connection.execute("SELECT COUNT(*) FROM inventory WHERE userid = ? AND item_id = ?",
                                         (user_id, item_id)) as cursor:
            count = await cursor.fetchone()
            item_count = int(count[0])

        if item_count > 0:
            await call.message.edit_text("✅ <b>Вы уже купили этот предмет.</b>", reply_markup=main_back())
        elif user_coins >= int(item[2]):
            await db.connection.execute(
                "INSERT INTO inventory (userid, item, description, item_id) VALUES (?, ?, ?, ?)",
                (user_id, item[0], item[1], item_id))
            await db.connection.execute("UPDATE users SET coins = coins - ? WHERE userid = ?", (item[2], user_id))
            await db.connection.commit()

            await call.message.edit_text(f"🎉 <b>Вы успешно купили {item[0]}!</b>", reply_markup=main_back())
        else:
            await call.message.edit_text("❗ <b>Недостаточно монет для покупки этого предмета!</b>",
                                         reply_markup=main_back())
    else:
        await call.message.edit_text("🚫 <b>Этот предмет уже распродали.</b>", reply_markup=main_back())


# Обработчик callback для удаления товара
@router.callback_query(ItemCallback.filter(F.action == "delete"))
async def delete_item(call: CallbackQuery, callback_data: ItemCallback):
    item_id = callback_data.item_id
    await db.connection.execute("DELETE FROM shop WHERE item_id = ?", (item_id,))
    await db.connection.commit()

    await call.message.edit_text(f"Предмет успешно удален.", reply_markup=main_back())


# Обработчик callback для изменения количества товара
@router.callback_query(ItemCallback.filter(F.action == "edit_amount"))
async def edit_item_amount_start(call: CallbackQuery, callback_data: ItemCallback, state: FSMContext):
    item_id = callback_data.item_id
    await state.update_data(item_id=item_id)
    await state.set_state(EditItem.waiting_for_new_amount)
    await call.message.edit_text(f"Введите новое количество для предмета:", reply_markup=None)


# Обработчик сообщения для изменения количества товара
@router.message(EditItem.waiting_for_new_amount)
async def edit_item_amount_received(message: Message, state: FSMContext):
    new_amount = message.text
    data = await state.get_data()
    item_id = data['item_id']

    await db.connection.execute("UPDATE shop SET amount = ? WHERE item_id = ?", (new_amount, item_id))
    await db.connection.commit()

    await state.clear()
    await message.answer(f"Количество предмета успешно изменено на {new_amount}.", reply_markup=main_back())
