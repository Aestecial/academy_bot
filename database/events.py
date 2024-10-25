from database.base import DataBase  # Импортируем класс DataBase из модуля database.base

# Создаем экземпляр базы данных
db = DataBase()


# Функция для создания или обновления события
async def create_event(name: str, text: str, max_participants: int) -> None:
    # Подключаемся к базе данных
    connector = await db.connect()
    try:
        # Выполняем SQL-запрос для обновления записи в таблице events, где id равен 1
        async with connector.execute(
                "INSERT INTO events (name, text, max_participants) VALUES (?, ?, ?)",
                (name, text, max_participants)
        ):
            # Подтверждаем изменения в базе данных
            await connector.commit()
    except Exception as e:
        # Обрабатываем возможные исключения и выводим сообщение об ошибке
        print(f"Произошла ошибка при вставке данных - {e}")


# Функция для получения событий
async def get_events():
    # Подключаемся к базе данных
    connector = await db.connect()
    try:
        # Выполняем SQL-запрос для получения всех записей из таблицы events
        async with connector.execute("SELECT * FROM events") as cursor:
            # Получаем первую строку результата
            row = await cursor.fetchall()
            if row:
                return row  # Возвращаем найденную строку
            return []  # Если строка не найдена, возвращаем False
    except Exception as e:
        # Обрабатываем возможные исключения и выводим сообщение об ошибке
        print(f"Произошла ошибка при получении роли пользователя - {e}")
        return "Error"


async def get_event(event_id: int):
    # Подключаемся к базе данных
    connector = await db.connect()
    try:
        # Выполняем SQL-запрос для получения всех записей из таблицы events
        async with connector.execute("SELECT * FROM events WHERE id = ?", (event_id,)) as cursor:
            # Получаем первую строку результата
            row = await cursor.fetchone()
            if row:
                return row  # Возвращаем найденную строку
            return False  # Если строка не найдена, возвращаем False
    except Exception as e:
        # Обрабатываем возможные исключения и выводим сообщение об ошибке
        print(f"Произошла ошибка при получении роли пользователя - {e}")
        return "Error"


# Функция для удаления всех заявок на мероприятия
async def delete_event_applications(event_id: int) -> None:
    # Подключаемся к базе данных
    connector = await db.connect()
    try:
        # Выполняем SQL-запрос для удаления всех записей из таблицы event_applications
        async with connector.execute("DELETE FROM event_applications WHERE event_id = ?", (event_id,)):
            # Подтверждаем изменения в базе данных
            await connector.commit()
        # Выполняем SQL-запрос для удаления всех записей из таблицы event_applications
        async with connector.execute("DELETE FROM events WHERE id = ?", (event_id,)):
            # Подтверждаем изменения в базе данных
            await connector.commit()
    except Exception as e:
        # Обрабатываем возможные исключения и выводим сообщение об ошибке
        print(f"Произошла ошибка при удалении заявок на мероприятия - {e}")
