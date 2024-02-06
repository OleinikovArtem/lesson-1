import sys
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram_dialog import setup_dialogs
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import common, address, services
from helpers.config_reader import config

import comands


bot = Bot(token=config.bot_token.get_secret_value(), parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())


async def main():
    dp.include_routers(common.router, address.router, services.dialog)
    setup_dialogs(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
