# Импортируем библиотеку aiosqlite для работы с асинхронным подключением к SQLite базе данных
import aiosqlite


# Определяем класс DataBase для управления подключением к базе данных
class DataBase:
    def __init__(self):
        self.connection = None

    async def connect(self) -> aiosqlite.Connection:
        try:
            if self.connection:
                await self.connection.close()
            self.connection = await aiosqlite.connect('data/base.db')
            return self.connection
        except Exception as _ex:
            print(f"Произошла ошибка с подключением БД - {_ex}")

    async def fetch_items(self, offset=0, limit=9):
        async with self.connection.execute(
                "SELECT name, description, price, amount, item_id FROM shop LIMIT ? OFFSET ?",
                (limit, offset)) as cursor:
            return await cursor.fetchall()

    async def get_user_role(self, userid):
        async with self.connection.execute("SELECT role FROM users WHERE userid = ?", (userid,)) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else None

    async def count_items(self):
        async with self.connection.execute("SELECT COUNT(*) FROM shop") as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0
