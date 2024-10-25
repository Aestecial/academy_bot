from database.base import DataBase  # Импортируем класс DataBase из модуля database.base

# Создаем экземпляр базы данных
db = DataBase()


# Функция для создания заявки
async def create_application(initials: str, username: str, userid: str, event_id: int) -> None:
    # Подключаемся к базе данных
    connector = await db.connect()
    try:
        # Выполняем SQL-запрос для вставки данных в таблицу event_applications
        async with connector.execute(
                "INSERT INTO event_applications (userid, username, initials, event_id) VALUES (?, ?, ?, ?)",
                (userid, username, initials, event_id)
        ):
            # Подтверждаем изменения в базе данных
            await connector.commit()
    except Exception as e:
        # Обрабатываем возможные исключения и выводим сообщение об ошибке
        print(f"Произошла ошибка при вставке данных - {e}")


# Функция для получения заявки пользователя по его ID
async def get_user_application(userid: str):
    # Подключаемся к базе данных
    connector = await db.connect()
    try:
        # Выполняем SQL-запрос для получения данных из таблицы event_applications
        async with connector.execute("SELECT * FROM event_applications WHERE userid = ?", (userid,)) as cursor:
            # Получаем первую строку результата
            row = await cursor.fetchone()
            if row:
                return row  # Возвращаем найденную строку
            else:
                return False  # Если строка не найдена, возвращаем False
    except Exception as e:
        # Обрабатываем возможные исключения и выводим сообщение об ошибке
        print(f"Произошла ошибка при получении роли пользователя - {e}")
        return "Error"


# Функция для получения заявок пользователей по их статусу
async def get_users_application(status: str):
    # Подключаемся к базе данных
    connector = await db.connect()
    try:
        # Выполняем SQL-запрос для получения данных из таблицы event_applications по статусу
        async with connector.execute("SELECT * FROM event_applications WHERE status = ?", (status,)) as cursor:
            # Получаем все строки результата
            row = await cursor.fetchall()
            if row:
                return row  # Возвращаем найденные строки
            else:
                return False  # Если строки не найдены, возвращаем False
    except Exception as e:
        # Обрабатываем возможные исключения и выводим сообщение об ошибке
        print(f"Произошла ошибка при получении роли пользователя - {e}")
        return "Error"


# Функция для получения всех заявок
async def get_all_applications():
    # Подключаемся к базе данных
    connector = await db.connect()
    try:
        # Выполняем SQL-запрос для получения всех данных из таблицы event_applications
        async with connector.execute("SELECT * FROM event_applications") as cursor:
            # Получаем все строки результата
            row = await cursor.fetchall()
            if row:
                return row  # Возвращаем найденные строки
            else:
                return []  # Если строки не найдены, возвращаем пустой список
    except Exception as e:
        # Обрабатываем возможные исключения и выводим сообщение об ошибке
        print(f"Произошла ошибка при получении роли пользователя - {e}")
        return "Error"


# Функция для удаления заявки пользователя по его ID
async def remove_user_application(userid: str):
    try:
        # Подключаемся к базе данных
        connector = await db.connect()
        # Выполняем SQL-запрос для удаления данных из таблицы event_applications по ID пользователя
        await connector.execute("DELETE FROM event_applications WHERE userid = ?", (userid,))
        # Подтверждаем изменения в базе данных
        await connector.commit()
    except Exception as e:
        # Обрабатываем возможные исключения и выводим сообщение об ошибке
        print(f"Произошла ошибка при удалении цели пользователя - {e}")
        return "Error"


# Функция для удаления всех заявок
async def remove_all_applications():
    try:
        # Подключаемся к базе данных
        connector = await db.connect()
        # Выполняем SQL-запрос для удаления всех данных из таблицы event_applications
        await connector.execute("DELETE FROM event_applications")
        # Подтверждаем изменения в базе данных
        await connector.commit()
    except Exception as e:
        # Обрабатываем возможные исключения и выводим сообщение об ошибке
        print(f"Произошла ошибка при удалении цели пользователя - {e}")
        return "Error"


# Функция для получения статуса заявки пользователя по его ID
async def get_application_status(userid: str):
    # Подключаемся к базе данных
    connector = await db.connect()
    try:
        # Выполняем SQL-запрос для получения статуса из таблицы event_applications по ID пользователя
        async with connector.execute("SELECT status FROM event_applications WHERE userid = ?", (userid,)) as cursor:
            # Получаем первую строку результата
            row = await cursor.fetchone()
            if row:
                return row[0]  # Возвращаем найденный статус
            else:
                return False  # Если строка не найдена, возвращаем False
    except Exception as e:
        # Обрабатываем возможные исключения и выводим сообщение об ошибке
        print(f"Произошла ошибка при получении роли пользователя - {e}")
        return "Error"


# Функция для получения всех организаторов
async def get_all_organizers():
    # Подключаемся к базе данных
    connector = await db.connect()
    try:
        # Выполняем SQL-запрос для получения данных из таблицы users, где роль равна "Организатор"
        async with connector.execute("SELECT userid FROM users WHERE role = \"Организатор\"") as cursor:
            # Получаем все строки результата
            row = await cursor.fetchall()
            if row:
                return row  # Возвращаем найденные строки
            else:
                return []  # Если строки не найдены, возвращаем пустой список
    except Exception as e:
        # Обрабатываем возможные исключения и выводим сообщение об ошибке
        print(f"Произошла ошибка при получении роли пользователя - {e}")
        return "Error"


# Функция для установки статуса заявки пользователя по его ID
async def set_application_status(userid: str, status: str):
    # Подключаемся к базе данных
    connector = await db.connect()
    try:
        # Выполняем SQL-запрос для обновления статуса в таблице event_applications по ID пользователя
        async with connector.execute(
                "UPDATE event_applications SET status = ? WHERE userid = ?",
                (status, userid)
        ):
            # Подтверждаем изменения в базе данных
            await connector.commit()
    except Exception as e:
        # Обрабатываем возможные исключения и выводим сообщение об ошибке
        print(f"Произошла ошибка при вставке данных - {e}")
