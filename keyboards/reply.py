from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def refactor_phone():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    manually = KeyboardButton(text='Ввести в ручную')
    contact = KeyboardButton(text='Отправить контакт', request_contact=True)
    markup.row(manually, contact)
    return markup


def generate_location():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    loc1 = KeyboardButton(text='Метро Айбека')
    markup.row(loc1)
    return markup


def generate_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    basket = KeyboardButton(text='📥 Корзина')
    sets = KeyboardButton(text='Наборы(сеты)')
    shaurma = KeyboardButton(text='🥙 Шаурма')
    side_dishes = KeyboardButton(text='🍟 Гарниры')
    hot_dogs = KeyboardButton(text='🌭 Хот-Доги')
    salads = KeyboardButton(text='🥗 Салаты')
    sous = KeyboardButton(text='🧂 Соусы')
    dessert = KeyboardButton(text='🍮 Десерты')
    ice_cream = KeyboardButton(text='🍨 Мороженое')
    lavash = KeyboardButton(text='🌯 Лаваш')
    burger = KeyboardButton(text='🍔 Бургеры')
    cool_drinks = KeyboardButton(text='🍹 Холодные напитки')
    hot_drinks = KeyboardButton(text='☕ Горячие напитки')
    snacks = KeyboardButton(text='Снеки')
    back = KeyboardButton(text='⬅ Назад')
    markup.row(sets)
    markup.row(shaurma, lavash)
    markup.row(burger, hot_dogs)
    markup.row(snacks, salads)
    markup.row(side_dishes, sous)
    markup.row(dessert, ice_cream)
    markup.row(cool_drinks, hot_drinks)
    markup.row(basket)
    markup.row(back)
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
