from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database.database import DataBase

bot = Bot('Token', parse_mode='HTML')
storage = MemoryStorage()
db = DataBase()
dp = Dispatcher(bot, storage=storage)
