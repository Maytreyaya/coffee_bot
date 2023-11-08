import asyncio
import logging
import sqlite3
from aiogram import Bot, Dispatcher
from handlers import orders, common, users

from config_reader import config


async def main():


    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()

    dp.include_routers(orders.router)
    dp.include_routers(common.router)
    dp.include_routers(users.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
