import asyncio
import logging
import os

from aiogram.utils import executor
from app.dbwork import db2Working
from aiogram import Bot
from aiogram.types import BotCommand
from app.handlers.location_state import register_handlers_find_loc
from app.handlers.common import register_handlers_common
from create_bot import dp, bot
from app import config


logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/update_personal", description="📝 Modify your register data"),
        BotCommand(command="/cancel", description="❌ Cancel the current action and get back to the main menu"),
        BotCommand(command="/time", description="⌚ Get aware about next approximate delivery time in your city ")
    ]
    await bot.set_my_commands(commands)


async def on_startup(dp):
    await bot.set_webhook(config.config(section="config").get("URL"))


async def on_shutdown(dp):
    await bot.delete_webhook()


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")
    await set_commands(bot)
    register_handlers_common(dp)
    register_handlers_find_loc(dp)
    #long polling
    await dp.skip_updates()
    await dp.start_polling()

    #webhook
    # executor.start_webhook(dispatcher=dp,
    #                        webhook_path='',
    #                        on_startup=on_startup,
    #                        on_shutdown=on_shutdown,
    #                        skip_updates=True,
    #                        host="0.0.0.0",
    #                        port=int(os.environ.get("PORT", 5000)))

if __name__ == '__main__':
    asyncio.run(main())



