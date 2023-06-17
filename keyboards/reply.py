from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data.loader import db


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


def generate_type_of_order():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    delivery = KeyboardButton(text='🚖 Доставка')
    pickup = KeyboardButton(text='🏃🏻‍♂️ Самовывоз')
    back = KeyboardButton(text='⬅ Назад')
    markup.row(delivery, pickup)
    markup.row(back)
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
    buttons = []
    for category in categories:
        btn = KeyboardButton(text=category)
        buttons.append(btn)
    markup.add(*buttons, main_mark, back, cart)
    return markup


def generate_filial():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back = KeyboardButton(text='⬅ Назад к доставке')
    filials = db.get_filials_names()
    buttons = []
    for filial in filials:
        btn = KeyboardButton(text=filial[0])
        buttons.append(btn)
    markup.add(*buttons)
    markup.add(back)
    return markup


def generate_delivery():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    location = KeyboardButton(text='🚩 Локация', request_location=True)
    my_address = KeyboardButton(text='🗺 Мои адреса')
    back = KeyboardButton(text='⬅ Назад')
    markup.row(location, my_address)
    markup.row(back)
    return markup


def generate_filials_info():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back = KeyboardButton(text='⬅ Назад к информации')
    filials = db.get_filials_names()
    buttons = []
    for filial in filials:
        btn = KeyboardButton(text='ℹ' + filial[0])
        buttons.append(btn)
    markup.add(*buttons)
    markup.add(back)
    return markup


def menu_information():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    back = KeyboardButton(text='⬅ Назад')
    filial = KeyboardButton(text='🏪 О филиалах')
    mobile_apps = KeyboardButton(text='📱 Мобильное приложение')
    about_us = KeyboardButton(text='📃 О нас')
    markup.row(filial)
    markup.row(mobile_apps, about_us)
    markup.row(back)
    return markup


def generate_review():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    back = KeyboardButton(text='⬅ Назад')
    bt1 = KeyboardButton(text='😤Хочу пожаловатся 👎🏻')
    bt2 = KeyboardButton(text='☹️Не понравилось, на 2 ⭐️⭐️')
    bt3 = KeyboardButton(text='😐Удовлетворительно на 3 ⭐️⭐️⭐️')
    bt4 = KeyboardButton(text='☺️Нормально, на 4 ⭐️⭐️⭐️⭐️')
    bt5 = KeyboardButton(text='😊Все понравилось, на 5 ❤️')
    markup.row(bt5)
    markup.row(bt4)
    markup.row(bt3)
    markup.row(bt2)
    markup.row(bt1)
    markup.row(back)
    return markup


def generate_products(category_title):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    back = KeyboardButton(text='⬅ Назад к категориям')
    cart = KeyboardButton(text='🛒 Корзина')
    products = db.get_products_by_category(category_title=category_title)
    buttons = []
    for product in products:
        btn = KeyboardButton(text=product[0])
        buttons.append(btn)
    markup.add(*buttons)
    markup.add(cart)
    markup.add(back)
    return markup
