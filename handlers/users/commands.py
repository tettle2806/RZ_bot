from aiogram.types import Message

from data.loader import dp, db
from .text_handlers import start_register, show_main_menu


@dp.message_handler(commands=['start'])
async def command_start(message: Message):
    await message.answer('Добро пожаловать')
    user = db.get_user_by_id(message.chat.id)
    if user:
        '''Показать главное меню'''
        await show_main_menu(message)
    else:
        await start_register(message)
    # Начало регистрации по номеру


@dp.message_handler(commands=['menu'])
async def command_menu(message: Message):
    await message.answer('https://telegra.ph/Nashe-Menyu-06-03-20')


@dp.message_handler(commands=['feedback'])
async def command_feedback(message: Message):
    await message.answer('<b>Единый call-center:</b> 1234 или +998(70) 123-45-67')
