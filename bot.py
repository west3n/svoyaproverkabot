from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot.database.sqlite import sqlite
from bot import config as cfg
import asyncio
import logging


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'[%(asctime)s] - %(message)s')
    cfg.logger.info("Starting bot")
    bot = Bot(cfg.bot_token, parse_mode="HTML")
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    cfg.register_handlers(dp)
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
