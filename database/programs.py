from database.base import DataBase  # Импортируем класс DataBase из модуля database.base

# Создаем экземпляр базы данных
db = DataBase()


# Функция для создания или обновления программы
async def create_program(text: str) -> None:
    # Подключаемся к базе данных
    connector = await db.connect()
    try:
        # Выполняем SQL-запрос для обновления записи в таблице program, где id равен 1
        async with connector.execute(
                "UPDATE program SET text = ? WHERE id = 1",
                (text,)
        ):
            # Подтверждаем изменения в базе данных
            await connector.commit()
    except Exception as e:
        # Обрабатываем возможные исключения и выводим сообщение об ошибке
        print(f"Произошла ошибка при вставке данных - {e}")


# Функция для получения программы
async def get_program():
    # Подключаемся к базе данных
    connector = await db.connect()
    try:
        # Выполняем SQL-запрос для получения всех записей из таблицы program
        async with connector.execute("SELECT * FROM program") as cursor:
            # Получаем первую строку результата
            row = await cursor.fetchone()
            if row:
                return row[-1]  # Возвращаем последний элемент строки, который содержит текст программы
            return False  # Если строка не найдена, возвращаем False
    except Exception as e:
        # Обрабатываем возможные исключения и выводим сообщение об ошибке
        print(f"Произошла ошибка при получении программы - {e}")
        return "Error"
