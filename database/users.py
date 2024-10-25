from database.base import DataBase  # Импортируем класс DataBase из модуля database.base

# Создаем экземпляр базы данных
db = DataBase()


# Функция для создания пользователя
async def create_user(initials: str, username: str, userid: str, role: str) -> None:
    # Подключаемся к базе данных
    connector = await db.connect()
    try:
        # Выполняем SQL-запрос для вставки новой записи в таблицу users
        async with connector.execute(
                "INSERT INTO users (initials, role, username, userid) VALUES (?, ?, ?, ?)",
                (initials, role, username, userid)
        ):
            # Подтверждаем изменения в базе данных
            await connector.commit()
    except Exception as e:
        # Обрабатываем возможные исключения и выводим сообщение об ошибке
        print(f"Произошла ошибка при вставке данных - {e}")


# Функция для получения инвентаря по наименованию предмета
async def get_item_inventory(item: str):
    # Подключаемся к базе данных
    connector = await db.connect()
    try:
        # Выполняем SQL-запрос для получения всех записей из таблицы inventory по наименованию предмета
        async with connector.execute("SELECT * FROM inventory WHERE item = ?", (item,)) as cursor:
            rows = await cursor.fetchall()
            if rows:
                return rows  # Возвращаем найденные строки
            else:
                return []  # Если строки не найдены, возвращаем пустой список
    except Exception as e:
        # Обрабатываем возможные исключения и выводим сообщение об ошибке
        print(f"Произошла ошибка при получении предмета в инвентаре - {e}")
        return []


# Функция для получения инвентаря пользователя по его ID
async def get_user_inventory(userid: str):
    # Подключаемся к базе данных
    connector = await db.connect()
    try:
        # Выполняем SQL-запрос для получения всех записей из таблицы inventory по ID пользователя
        async with connector.execute("SELECT * FROM inventory WHERE userid = ?", (userid,)) as cursor:
            rows = await cursor.fetchall()
            if rows:
                return rows  # Возвращаем найденные строки
            else:
                return []  # Если строки не найдены, возвращаем пустой список
    except Exception as e:
        # Обрабатываем возможные исключения и выводим сообщение об ошибке
        print(f"Произошла ошибка при получении инвентаря пользователя - {e}")
        return []


# Функция для получения роли пользователя по его ID
async def get_user_role(userid: str):
    # Подключаемся к базе данных
    connector = await db.connect()
    try:
        # Выполняем SQL-запрос для получения роли пользователя из таблицы users по ID
        async with connector.execute("SELECT role FROM users WHERE userid = ?", (userid,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return row[0]  # Возвращаем найденную роль
            else:
                return []  # Если строка не найдена, возвращаем False
    except Exception as e:
        # Обрабатываем возможные исключения и выводим сообщение об ошибке
        print(f"Произошла ошибка при получении роли пользователя - {e}")
        return "Error"


# Функция для установки рейтинга пользователя
async def set_user_rating(userid: str, rating: float):
    # Подключаемся к базе данных
    connector = await db.connect()
    try:
        # Выполняем SQL-запрос для обновления рейтинга пользователя в таблице users по ID
        async with connector.execute(
                "UPDATE users SET rating = ? WHERE userid = ?",
                (rating, userid)
        ):
            # Подтверждаем изменения в базе данных
            await connector.commit()
    except Exception as e:
        # Обрабатываем возможные исключения и выводим сообщение об ошибке
        print(f"Произошла ошибка при вставке данных - {e}")


# Функция для получения количества монет пользователя
async def get_user_coins(userid: str):
    # Подключаемся к базе данных
    connector = await db.connect()
    try:
        # Выполняем SQL-запрос для получения количества монет пользователя из таблицы users по ID
        async with connector.execute("SELECT coins FROM users WHERE userid = ?", (userid,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return row[0]  # Возвращаем количество монет
            else:
                return []  # Если строка не найдена, возвращаем False
    except Exception as e:
        # Обрабатываем возможные исключения и выводим сообщение об ошибке
        print(f"Произошла ошибка при получении монет пользователя - {e}")
        return "Error"


# Функция для установки количества монет пользователя
async def set_user_coins(userid: str, coin: int):
    # Подключаемся к базе данных
    connector = await db.connect()
    try:
        # Выполняем SQL-запрос для обновления количества монет пользователя в таблице users по ID
        async with connector.execute(
                "UPDATE users SET coins = ? WHERE userid = ?",
                (coin, userid)
        ):
            # Подтверждаем изменения в базе данных
            await connector.commit()
    except Exception as e:
        # Обрабатываем возможные исключения и выводим сообщение об ошибке
        print(f"Произошла ошибка при вставке данных - {e}")


# Функция для установки уровня пользователя
async def set_user_level(userid: str, level: int):
    # Подключаемся к базе данных
    connector = await db.connect()
    try:
        # Выполняем SQL-запрос для обновления уровня пользователя в таблице users по ID
        async with connector.execute(
                "UPDATE users SET level = ? WHERE userid = ?",
                (level, userid)
        ):
            # Подтверждаем изменения в базе данных
            await connector.commit()
    except Exception as e:
        # Обрабатываем возможные исключения и выводим сообщение об ошибке
        print(f"Произошла ошибка при вставке данных - {e}")


# Функция для получения ID пользователей для рассылки по роли и уровню
async def get_user_mailing(role: str, level: int):
    # Подключаемся к базе данных
    connector = await db.connect()
    try:
        # Выполняем SQL-запрос для получения всех ID пользователей из таблицы users по роли и уровню
        async with connector.execute("SELECT userid FROM users WHERE role = ? AND level = ?", (role, level)) as cursor:
            rows = await cursor.fetchall()
            if rows:
                return rows  # Возвращаем найденные строки
            else:
                return []  # Если строки не найдены, возвращаем пустой список
    except Exception as e:
        # Обрабатываем возможные исключения и выводим сообщение об ошибке
        print(f"Произошла ошибка при получении айди пользователя - {e}")
        return "Error"


# Функция для получения ID пользователей для рассылки по роли без учета уровня
async def get_user_mailing_without_level(role: str):
    # Подключаемся к базе данных
    connector = await db.connect()
    try:
        # Выполняем SQL-запрос для получения всех ID пользователей из таблицы users по роли
        async with connector.execute("SELECT userid FROM users WHERE role = ?", (role,)) as cursor:
            rows = await cursor.fetchall()
            if rows:
                return rows  # Возвращаем найденные строки
            else:
                return []  # Если строки не найдены, возвращаем False
    except Exception as e:
        # Обрабатываем возможные исключения и выводим сообщение об ошибке
        print(f"Произошла ошибка при получении айди пользователя - {e}")
        return "Error"


# Функция для получения ID всех пользователей для рассылки
async def get_all_user_mailing():
    # Подключаемся к базе данных
    connector = await db.connect()
    try:
        # Выполняем SQL-запрос для получения всех ID пользователей из таблицы users
        async with connector.execute("SELECT userid FROM users") as cursor:
            rows = await cursor.fetchall()
            if rows:
                return rows  # Возвращаем найденные строки
            else:
                return []  # Если строки не найдены, возвращаем False
    except Exception as e:
        # Обрабатываем возможные исключения и выводим сообщение об ошибке
        print(f"Произошла ошибка при получении айди пользователя - {e}")
        return "Error"


# Функция для получения данных пользователя по его ID
async def get_user(userid: str):
    # Подключаемся к базе данных
    connector = await db.connect()
    try:
        # Выполняем SQL-запрос для получения всех данных пользователя из таблицы users по ID
        async with connector.execute("SELECT * FROM users WHERE userid = ?", (userid,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return row  # Возвращаем найденную строку
            else:
                return False  # Если строка не найдена, возвращаем False
    except Exception as e:
        # Обрабатываем возможные исключения и выводим сообщение об ошибке
        print(f"Произошла ошибка при получении пользователя - {e}")
        return "Error"


# Функция для получения рейтинга всех делегатов
async def get_rating():
    # Подключаемся к базе данных
    connector = await db.connect()
    try:
        # Выполняем SQL-запрос для получения рейтинга всех делегатов из таблицы users
        async with connector.execute(
                'SELECT rating, userid, username, initials FROM users WHERE role = "Делегат"') as cursor:
            row = await cursor.fetchall()
            if row:
                return row  # Возвращаем найденные строки
            else:
                return []  # Если строки не найдены, возвращаем False
    except Exception as e:
        # Обрабатываем возможные исключения и выводим сообщение об ошибке
        print(f"Произошла ошибка при получении рейтинга пользователей - {e}")
        return "Error"


# Функция для получения целей пользователя по его ID
async def get_goals(userid: str):
    # Подключаемся к базе данных
    connector = await db.connect()
    try:
        # Выполняем SQL-запрос для получения всех целей пользователя из таблицы goals по ID
        async with connector.execute("SELECT goal FROM goals WHERE userid = ?", (userid,)) as cursor:
            row = await cursor.fetchall()
            if row:
                return row  # Возвращаем найденные строки
            else:
                return False  # Если строки не найдены, возвращаем False
    except Exception as e:
        # Обрабатываем возможные исключения и выводим сообщение об ошибке
        print(f"Произошла ошибка при получении цели пользователя - {e}")
        return "Error"


# Функция для обновления имени пользователя
async def update_username(userid: str, username: str):
    try:
        # Подключаемся к базе данных
        connector = await db.connect()
        # Выполняем SQL-запрос для обновления имени пользователя в таблице users по ID
        await connector.execute("UPDATE users SET username = ? WHERE userid = ?", (username, userid))
        # Подтверждаем изменения в базе данных
        await connector.commit()
    except Exception as e:
        # Обрабатываем возможные исключения и выводим сообщение об ошибке
        print(f"Произошла ошибка при изменении username пользователя - {e}")
        return "Error"


# Функция для обновления инициалов пользователя
async def update_initials(userid: str, initials: str):
    try:
        # Подключаемся к базе данных
        connector = await db.connect()
        # Выполняем SQL-запрос для обновления инициалов пользователя в таблице users по ID
        await connector.execute("UPDATE users SET initials = ? WHERE userid = ?", (initials, userid))
        # Подтверждаем изменения в базе данных
        await connector.commit()
    except Exception as e:
        # Обрабатываем возможные исключения и выводим сообщение об ошибке
        print(f"Произошла ошибка при изменении инициалов пользователя - {e}")
        return "Error"


# Функция для удаления делегата
async def delete_delegate(userid: str):
    try:
        # Подключаемся к базе данных
        connector = await db.connect()
        # Выполняем SQL-запрос для удаления пользователя из таблицы users по ID
        await connector.execute("DELETE FROM users WHERE userid = ?", (userid,))
        await connector.execute("DELETE FROM goals WHERE userid = ?", (userid,))
        await connector.execute("DELETE FROM event_applications WHERE userid = ?", (userid,))
        await connector.execute("DELETE FROM inventory WHERE userid = ?", (userid,))
        await connector.execute("DELETE FROM stars WHERE userid = ?", (userid,))
        # Подтверждаем изменения в базе данных
        await connector.commit()
    except Exception as e:
        # Обрабатываем возможные исключения и выводим сообщение об ошибке
        print(f"Произошла ошибка при удалении делегата - {e}")
        return "Error"


# Функция для удаления цели пользователя
async def delete_goal(userid: str, goal: str):
    try:
        # Подключаемся к базе данных
        connector = await db.connect()
        # Выполняем SQL-запрос для удаления цели пользователя из таблицы goals по ID и цели
        await connector.execute("DELETE FROM goals WHERE userid=? AND goal=?", (userid, goal))
        # Подтверждаем изменения в базе данных
        await connector.commit()
    except Exception as e:
        # Обрабатываем возможные исключения и выводим сообщение об ошибке
        print(f"Произошла ошибка при удалении цели пользователя - {e}")
        return "Error"


# Функция для удаления пользователя
async def deleted_user(userid: str):
    try:
        # Подключаемся к базе данных
        connector = await db.connect()
        # Выполняем SQL-запрос для удаления цели пользователя из таблицы goals по ID и цели
        await connector.execute("DELETE FROM users WHERE userid=?", (userid, ))
        # Подтверждаем изменения в базе данных
        await connector.commit()
    except Exception as e:
        # Обрабатываем возможные исключения и выводим сообщение об ошибке
        print(f"Произошла ошибка при удалении цели пользователя - {e}")
        return "Error"


# Функция для создания цели пользователя
async def create_goal(goal: str, userid: str) -> None:
    # Подключаемся к базе данных
    connector = await db.connect()
    try:
        # Выполняем SQL-запрос для вставки новой цели в таблицу goals
        async with connector.execute(
                "INSERT INTO goals (userid, goal) VALUES (?, ?)",
                (userid, goal)
        ):
            # Подтверждаем изменения в базе данных
            await connector.commit()
    except Exception as e:
        # Обрабатываем возможные исключения и выводим сообщение об ошибке
        print(f"Произошла ошибка при вставке данных - {e}")
