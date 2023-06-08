import re

from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.types import ReplyKeyboardRemove

from data.loader import dp, db
from keyboards.inline import generate_menu_language
from keyboards.reply import generate_main_menu, settings
from states.states import NumberState


async def start_register(message: Message, state=None):
    """
    Начало регистрации
    :param message:
    :param state:
    :return:
    """
    await NumberState.phone.set()
    await message.answer('Введите номер телефона в формате: +998 ** *** ** **')


@dp.message_handler(state=NumberState.phone)
async def get_phone(message: Message, state: FSMContext):
    """
    Проверка номера телефона
    если номер присутствует в базе данных то операция регистрации скипается,
    если же номера телефона нет он записывается вместе с остальными данными о пользователе

    :param message:
    :param state:
    :return:
    """

    phone = message.text
    result1 = re.search(r'\+998 \d\d \d\d\d \d\d \d\d', phone)
    result2 = re.search(r'\+998\d{9}', phone)
    if result1 or result2:
        await state.finish()
        chat_id = message.chat.id
        full_name = message.from_user.full_name
        db.insert_user(chat_id, full_name, phone)
        """Показать главное меню"""
        await show_main_menu(message)
    else:
        await state.finish()
        await again_ask_phone(message)


@dp.message_handler(regexp='📍 Язык')
async def reaction_on_language(message: Message):
    re = ReplyKeyboardRemove()
    await message.answer('Выберите язык', reply_markup=generate_menu_language())


@dp.message_handler(regexp='⚙ Настройки')
async def reaction_settings(message: Message):
    """
    Функционал кнопки НАСТРОЙКИ
    :param message:
    :return:
    """
    await message.answer('Выберите что хотите сделать', reply_markup=settings())


@dp.message_handler(regexp='⬅ Назад')
async def reaction_settings(message: Message):
    """
    Функционал кнопки назад
    :param message:
    :return:
    """
    await message.answer('Главное меню', reply_markup=generate_main_menu())


async def again_ask_phone(message: Message, state=None):
    """
    Функция, которая переспрашивает номер телефона если тот был введен неверно
    :param message:
    :param state:
    :return:
    """
    await NumberState.phone.set()
    await message.answer('''Не верный формат телефона.
Введите номер телефона в формате: +998 ** *** ** **''')


async def show_main_menu(message: Message):
    """
    Функция возврата на главное меню
    :param message:
    :return:
    """
    await message.answer('Главное меню', reply_markup=generate_main_menu())
