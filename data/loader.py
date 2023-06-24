from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database.database import DataBase

bot = Bot('6094431594:AAEVBt9BDjFzna5ZPcj6ZyB-MD3PqP1MILI', parse_mode='HTML')
storage = MemoryStorage()
db = DataBase()
dp = Dispatcher(bot, storage=storage)
