import configparser

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os


config = configparser.ConfigParser()
config.read("config/bot.ini")
bot = Bot(config.get("config", "TOKEN"))
dp = Dispatcher(bot, storage=MemoryStorage())