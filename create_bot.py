import configparser

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.mongo import MongoStorage

config = configparser.ConfigParser()
config.read("config/bot.ini")
bot = Bot(config.get("config", "TOKEN"))

storage = MongoStorage(db_name='PythonPollStates', uri=config.get("mongoDB", "uri"))
dp = Dispatcher(bot, storage=storage)
