from aiogram.types import Message
from data.loader import bot, dp, db
from .text_handlers import start_register, show_main_menu


@dp.message_handler(commands=['start'])
async def command_start(message: Message):
    """
    Реакция на команду старт,
    с дальнейшей проверкой через базу данных,
    если зарегистрирован показываем главное меню,
    иначе начинаем регистрацию

    :param message:
    :return:
    """
    await message.answer('Добро пожаловать в мир рыбы и хлеба')
    user = db.get_user_by_id(message.chat.id)
    if user:
        await show_main_menu(message)
    else:
        await start_register(message)


@dp.message_handler(commands=['menu'])
async def command_menu(message: Message):
    """
    Реакция на команду меню

    :param message:
    :return:
    """
    await message.answer('https://telegra.ph/Nashe-Menyu-06-03-20')


@dp.message_handler(commands=['feedback'])
async def command_feedback(message: Message):
    """
    Реакция на команду отзывы
    :param message:
    :return:
    """
    await message.answer('<b>Единый call-center:</b> 1234 или +998(70) 123-45-67')
