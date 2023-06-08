from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def generate_menu_language():
    """
    Генерирует инлайн кнопки для смены языка

    :return:
    """
    markup = InlineKeyboardMarkup(row_width=1)
    ibt1 = InlineKeyboardButton(text='Русский',
                                callback_data='ru')
    ibt2 = InlineKeyboardButton(text='English',
                                callback_data='en')
    markup.add(ibt1, ibt2)
    return markup
