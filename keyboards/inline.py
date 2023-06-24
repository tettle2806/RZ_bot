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


def generate_product_details(product_id, quantity=1):
    markup = InlineKeyboardMarkup()
    minus_button = InlineKeyboardButton('➖', callback_data='minus')
    quan_button = InlineKeyboardButton(str(quantity), callback_data=f'quantity_{product_id}')
    plus_btn = InlineKeyboardButton('➕', callback_data='plus')
    buy_btn = InlineKeyboardButton('Хочу 🐱', callback_data=f'buy_{product_id}_{quantity}')
    cart_btn = InlineKeyboardButton('🛒 Корзина', callback_data='cart')
    markup.add(minus_button, quan_button, plus_btn)
    markup.add(buy_btn)
    markup.add(cart_btn)
    return markup
