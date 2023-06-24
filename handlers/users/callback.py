from data.loader import bot, dp, db
from aiogram.types import CallbackQuery
from keyboards.inline import generate_product_details, \
    generate_menu_language


@dp.callback_query_handler(lambda call: call.data == 'plus')
async def reaction_to_plus(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    buttons = call.message.reply_markup.inline_keyboard
    quantity = int(buttons[0][1].text)
    product_id = buttons[0][1].callback_data.split('_')[1]
    if quantity < 5:
        quantity += 1
        await bot.edit_message_reply_markup(chat_id, message_id,
                                            reply_markup=generate_product_details(product_id, quantity))
    else:
        await bot.answer_callback_query(call.id,
                                        'Вы не можете купить бльше 5 товаров одного наименования')


@dp.callback_query_handler(lambda call: call.data == 'minus')
async def reaction_to_minus(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    buttons = call.message.reply_markup.inline_keyboard
    quantity = int(buttons[0][1].text)
    product_id = buttons[0][1].callback_data.split('_')[1]
    if quantity > 1:
        quantity -= 1
        await bot.edit_message_reply_markup(chat_id, message_id,
                                            reply_markup=generate_product_details(product_id, quantity))
    else:
        await bot.answer_callback_query(call.id,
                                        'Количество товаров не может равнятся 0')


@dp.callback_query_handler((lambda call: 'buy' in call.data))
async def add_product_to_cart(call: CallbackQuery):
    chat_id = call.message.chat.id
    _, product_id, quantity = call.data.split('_')
    print(product_id)
    product_title, price = db.get_product_by_id(product_id)
    print(product_title, price)
    final_price = int(quantity) * int(price)
    print(final_price)
    if db.get_cart_id(chat_id):
        cart_id = db.get_cart_id(chat_id)[0]
    else:
        db.create_cart_for_user(chat_id)
        cart_id = db.get_cart_id(chat_id)[0]

    try:
        '''Пытаемся закинуть новый товар в корзину'''
        db.insert_cart_product(cart_id, product_title, quantity, final_price)
        await bot.answer_callback_query(call.id, '''Товар успешно добавлен в корзину''')
    except Exception as e:
        print(e)
        '''Если такой товар был то обнавляем его цену и количество'''
        db.update_cart_product(cart_id, product_title, quantity, final_price)
        await bot.answer_callback_query(call.id, '''Количество успешно изменено''')
