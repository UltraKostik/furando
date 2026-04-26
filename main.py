#Telegram бот Фурандо, Furando. Разработчик @UltraKostik#

import asyncio
import logging
import os
import sys
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from aiogram.types import ErrorEvent
import handlers as hd
from database import init_db

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler('bot.log', encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    return logger

logger = setup_logger(__name__) 

def load_config():
    try:
        load_dotenv()
        token = os.getenv('BOT_TOKEN')
        if not token:
            logger.error("BOT_TOKEN отсутствует в .env файле")
            return None
        return token
    except Exception:
        logger.exception("Ошибка при загрузке конфигурации")
        return None

async def main():
    await init_db()
    logger.info("Запуск бота")
    token = load_config()
    if not token:
        logger.error("Не удалось загрузить конфигурацию. Бот остановлен.")
        return
    
    bot = None
    try:
        bot = Bot(token=token)
        dp = Dispatcher()
        dp.include_router(hd.router)
        @dp.errors()
        async def handle_errors(event: ErrorEvent):
            logger.exception("Глобальная ошибка")
            if event.update.message:
                await event.update.message.answer(
                    "❌ Произошла ошибка. Попробуйте позже."
                )
            return True
        logger.info("Бот успешно инициализирован")
        logger.info("Запуск polling...")
        await dp.start_polling(bot)
    except Exception:
        logger.exception("Ошибка во время работы бота")
    finally:
        if bot:
            await bot.session.close()
            logger.info("Сессия бота закрыта")
    
    logger.info("Бот завершил работу")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception:
        logger.exception("Критическая ошибка при запуске бота")