from data.loader import bot, dp, db
from aiogram.types import CallbackQuery, ShippingOption, LabeledPrice, Message
from keyboards.inline import generate_product_details, \
    generate_menu_language, generate_cart_buttons
from keyboards.reply import generate_main_menu


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


@dp.callback_query_handler(lambda call: 'remove' in call.data)
async def minus_inline(call: CallbackQuery):
    inf = call.inline_message_id

    print(inf)


@dp.callback_query_handler(lambda call: 'append' in call.data)
async def plus_inline(call: CallbackQuery):
    inf1 = call.data
    print(inf1)


@dp.callback_query_handler(lambda call: 'cart' == call.data)
async def show_cart(call: CallbackQuery):
    chat_id = call.message.chat.id
    if db.get_cart_id(chat_id):
        cart_id = db.get_cart_id(chat_id)[0]
    else:
        db.create_cart_for_user(chat_id)
        cart_id = db.get_cart_id(chat_id)[0]
    # Обновить общее количество и общую сумму
    # вытащить их потом вытащить все товары в корзине
    # сформировать сообщение и отправить пользователю
    db.update_cart_total_price_quantity(cart_id)
    total_price, total_quantity = db.get_cart_total_price_quantity(cart_id)
    try:
        total_price, total_quantity = int(total_price), int(total_quantity)
    except:
        total_price, total_quantity = 0, 0
    cart_product = db.get_cart_products_by_cart_id(cart_id)

    text = '''Ваша корзина\n\n'''
    print(total_price, total_quantity, cart_product)
    for cart_produc in cart_product:
        text += f'{cart_produc[2]} - {cart_produc[4]} шт - {cart_produc[3]} сум \n\n'

    text += f'''Общее колличество:{total_quantity} шт
Общая стоимость: {total_price} сум'''
    await bot.send_message(chat_id, text, reply_markup=generate_cart_buttons(cart_product, cart_id))


@dp.callback_query_handler(lambda call: 'main_menu' == call.data)
async def show_mainm_menu(call: CallbackQuery):
    await bot.send_message(chat_id=call.message.chat.id, text='Главное меню', reply_markup=generate_main_menu())


@dp.callback_query_handler(lambda call: 'order' in call.data)
async def payment(call: CallbackQuery):
    chat_id = call.message.chat.id
    cart_id = call.data.split('_')[1]
    products = db.get_cart_products_by_cart_id(cart_id)

    await bot.send_invoice(chat_id=chat_id,
                           title=f'Чек для {call.message.from_user.full_name}',
                           description=''.join([f'{product[2]}\n' for product in products]),
                           payload='shop_bot',
                           start_parameter='create_invoice_products',
                           currency='UZS',
                           prices=[
                               LabeledPrice(
                                   label=f'{product[2]} - {product[4]} шт',
                                   amount=int(product[3] * 100)
                               ) for product in products
                           ],
                           provider_token='398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065',
                           need_name=True,
                           need_shipping_address=True,
                           is_flexible=True,

                           )


EXPRESS_SHIPPING = ShippingOption(
    id='post_express',
    title='До 1 часа'
).add(LabeledPrice(label='До 1 часа', amount=20_000_00))

REGULAR_SHIPPING = ShippingOption(
    id='post_regular',
    title='Самовывоз'
).add(LabeledPrice(label='Самовывоз', amount=0))


@dp.shipping_query_handler(lambda query: True)
async def shippind(shipping_query):
    await bot.answer_shipping_query(shipping_query.id,
                                    ok=True,
                                    shipping_options=[EXPRESS_SHIPPING, REGULAR_SHIPPING],
                                    error_message='Простите что то не так')


@dp.pre_checkout_query_handler(lambda query: True)
async def checkout(pre):
    await bot.answer_pre_checkout_query(pre.id,
                                        ok=True,
                                        error_message='Опять что-то не так')


@dp.message_handler(content_types=['successful_payment'])
async def success_pay(message: Message):
    # Отправить админу сообщение со всей информацией о заказе
    await bot.send_message(message.chat.id, 'Оплата прошла успешно')
