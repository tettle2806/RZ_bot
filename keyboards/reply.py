from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from database.database import DataBase
from data.loader import db


def refactor_phone():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    manually = KeyboardButton(text='Ввести в ручную')
    contact = KeyboardButton(text='Отправить контакт', request_contact=True)
    back = KeyboardButton(text='⬅ Назад')
    markup.row(manually, contact)
    markup.row(back)
    return markup


def generate_menu_categories():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back = KeyboardButton(text='🚩 К филиалам')
    cart = KeyboardButton(text='🛒 Корзина')
    main_mark = KeyboardButton(text='⬅ Назад')
    categories = [i[0] for i in db.get_categories()]
    buuttons = []
    for category in categories:
        btn = KeyboardButton(text=category)
        buuttons.append(btn)
    markup.add(*buuttons, main_mark, back, cart)
    return markup


def generate_filials():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back = KeyboardButton(text='⬅ Назад')
    filials = db.get_filials_names()
    buttons = []
    for filial in filials:
        btn = KeyboardButton(text=filial[0])
        buttons.append(btn)
    markup.add(*buttons)
    markup.add(back)
    return markup


def generate_type_of_order():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    delivery = KeyboardButton(text='🚖 Доставка')
    pickup = KeyboardButton(text='🏃🏻‍♂️ Самовывоз')
    back = KeyboardButton(text='⬅ Назад')
    markup.row(delivery, pickup)
    markup.row(back)
    return markup


def generate_delivery():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    location = KeyboardButton(text='🚩 Локация', request_location=True)
    my_address = KeyboardButton(text='🗺 Мои адреса')
    back = KeyboardButton(text='⬅ Назад')
    markup.row(location, my_address)
    markup.row(back)
    return markup


def generate_main_menu():
    """
    Кнопки главного меню
    :return:
    """
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    order = KeyboardButton(text='🛍 Заказать')
    review = KeyboardButton(text='✍ Оставить отзыв')
    feedback = KeyboardButton(text='☎ Связаться с нами')
    info = KeyboardButton(text='ℹ Информация')
    settings = KeyboardButton(text='⚙ Настройки')
    markup.row(order)
    markup.row(review, feedback)
    markup.row(info, settings)
    return markup


def settings():
    """
    Кнопки меню настройки
    :return:
    """
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    refresh_fio = KeyboardButton(text='Изменить ФИО')
    refresh_number = KeyboardButton(text='Изменить номер')
    language = KeyboardButton(text='📍 Язык')
    back = KeyboardButton(text='⬅ Назад')
    markup.row(refresh_fio, refresh_number)
    markup.row(language)
    markup.row(back)
    return markup


def generate_filials_info():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back = KeyboardButton(text='⬅ Назад')
    filials = db.get_filials_names()
    buttons = []
    for filial in filials:
        btn = KeyboardButton(text='ℹ' + filial[0])
        buttons.append(btn)
    markup.add(*buttons)
    markup.add(back)
    return markup
