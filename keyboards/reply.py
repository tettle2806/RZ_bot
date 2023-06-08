from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


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
