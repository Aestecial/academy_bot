from database.base import DataBase  # Импортируем класс DataBase из модуля database.base

# Создаем экземпляр базы данных
db = DataBase()


# Функция для добавления звезды пользователю
async def add_stars(star: int, userid: int) -> None:
    # Подключаемся к базе данных
    connector = await db.connect()
    try:
        # Выполняем SQL-запрос для вставки новой записи в таблицу stars
        async with connector.execute(
                "INSERT INTO stars (userid, star) VALUES (?, ?)",
                (userid, star)
        ):
            # Подтверждаем изменения в базе данных
            await connector.commit()
    except Exception as e:
        # Обрабатываем возможные исключения и выводим сообщение об ошибке
        print(f"Произошла ошибка при вставке данных - {e}")


# Функция для получения всех звезд пользователя по его ID
async def get_user_stars(userid: int):
    # Подключаемся к базе данных
    connector = await db.connect()
    try:
        # Выполняем SQL-запрос для получения всех звезд пользователя из таблицы stars
        async with connector.execute("SELECT star FROM stars WHERE userid = ?", (userid,)) as cursor:
            # Получаем все строки результата
            rows = await cursor.fetchall()
            if rows:
                return rows  # Возвращаем найденные строки
            else:
                return False  # Если строки не найдены, возвращаем False
    except Exception as e:
        # Обрабатываем возможные исключения и выводим сообщение об ошибке
        print(f"Произошла ошибка при получении звезд пользователя - {e}")
        return "Error"
