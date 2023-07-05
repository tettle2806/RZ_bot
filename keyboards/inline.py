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


def generate_cart_buttons(cart_product, cart_id):
    markup = InlineKeyboardMarkup()
    # (4, 1, 'Kids-Комбо', 40000, 1)
    for cart_produc in cart_product:
        name = InlineKeyboardButton(text=cart_produc[2], callback_data='name')
        minus = InlineKeyboardButton(text='-1', callback_data=f'remove_{cart_produc[0]}')
        quan = InlineKeyboardButton(text=str(cart_produc[4]), callback_data='quan')
        plus = InlineKeyboardButton(text='+1', callback_data=f'append_{cart_produc[0]}')
        markup.row(name)
        markup.row(minus, quan, plus)
    clear = InlineKeyboardButton(text='Очистить', callback_data='clear')
    order = InlineKeyboardButton(text='Купить', callback_data=f'order_{cart_id}')
    main_menu = InlineKeyboardButton(text='Главное меню', callback_data='main_menu')
    markup.row(clear, order)
    markup.row(main_menu)
    return markup
