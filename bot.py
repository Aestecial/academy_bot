# Импортируем необходимые библиотеки и модули
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from config import Config, load_config

# Импортируем обработчики для разных типов пользователей и действий
from handlers.users import (
    registration,
    start,
    pulse,
    programs,
)

from handlers.delegate import (
    profile,
    shop
)

from handlers.organizer import (
    create_event,
    mailing,
    interaction_delegate,
    create_programs,
    event_signup
)

from handlers.guest import (
    delegate_rating,
    write_organizer,
    delete_user
)

# Настраиваем logger для логирования событий
logger = logging.getLogger(__name__)


# Основная асинхронная функция для запуска бота
async def main():
    # Настройка базового логирования
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
    logger.info("Запуск бота.")

    # Загрузка конфигурации из файла
    config: Config = load_config()
    # Инициализация бота с API_TOKEN и настройкой parse_mode для HTML
    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode="HTML")
    )
    # Использование памяти для хранения состояний FSM
    storage = MemoryStorage()

    # Создание диспетчера для обработки сообщений
    dp = Dispatcher(storage=storage)

    # Регистрация routers (обработчиков) для разных частей бота
    dp.include_router(registration.router)
    dp.include_router(start.router)
    dp.include_router(pulse.router)
    dp.include_router(programs.router)
    dp.include_router(profile.router)
    dp.include_router(create_event.router)
    dp.include_router(mailing.router)
    dp.include_router(delegate_rating.router)
    dp.include_router(interaction_delegate.router)
    dp.include_router(create_programs.router)
    dp.include_router(event_signup.router)
    dp.include_router(shop.router)
    dp.include_router(write_organizer.router)
    dp.include_router(delete_user.router)

    # Удаление webhook (если есть) и сброс ожидания обновлений
    await bot.delete_webhook(drop_pending_updates=True)
    # Запуск polling (опроса) Telegram API для получения обновлений
    await dp.start_polling(bot)


# Точка входа в программу
if __name__ == '__main__':
    # Запуск основной функции с помощью asyncio
    asyncio.run(main=main())
