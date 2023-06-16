import re

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from data.loader import dp, db, bot
from keyboards.inline import generate_menu_language
from keyboards.reply import \
    generate_main_menu, \
    settings, \
    generate_type_of_order, \
    generate_delivery, \
    generate_menu_categories, \
    generate_filial, \
    generate_filials_info, \
    generate_review, \
    menu_information
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


@dp.message_handler(regexp='✍ Оставить отзыв')
async def reaction_review(message: Message):
    await message.answer('✅Контроль сервиса доставки RZ fast food\n'
                         'Мы благодарим за сделанный выбор и будем рады, '
                         'если Вы поможете улучшить качество нашего сервиса!\n'
                         'Оцените нашу работу по 5 бальной шкале',
                         reply_markup=generate_review())


@dp.message_handler(regexp='☎ Связаться с нами')
async def reaction_feedback(message: Message):
    await message.answer('<b>Единый call-center:</b> 1234 или +998(70) 123-45-67')


@dp.message_handler(regexp='⚙ Настройки')
async def reaction_settings(message: Message):
    """
    Функционал кнопки НАСТРОЙКИ
    :param message:
    :return:
    """
    await message.answer('Выберите что хотите сделать',
                         reply_markup=settings())


@dp.message_handler(regexp='ℹ Информация')
async def generate_menu_information(message: Message):
    await message.answer('Какую информацию вы хотите получить?',
                         reply_markup=menu_information())


@dp.message_handler(regexp='🏪 О филиалах')
async def filial_information(message: Message):
    await message.answer('Выберите филиал', reply_markup=generate_filials_info())


@dp.message_handler(regexp='📱 Мобильное приложение')
async def mobile_app(message: Message):
    await message.answer('Мобильное приложение еще в разработке, '
                         'приносим извинения', reply_markup=menu_information())


@dp.message_handler(regexp='📃 О нас')
async def about_us(message: Message):
    pic = open('logoRZ.png', mode='rb')
    text = f'Компания быстрого питания RZ FAST FOOD - это сеть ресторанов быстрого питания,\
которая специализируется на предоставлении разнообразных блюд быстрого приготовления.\
\n\nКомпания была создана в 2010 году и быстро стала одним из самых популярных ресторанов быстрого питания.\
\n\nRZ FAST FOOD предлагает широкий выбор блюд, включая гамбургеры, сэндвичи,\
картофель фри, напитки и другие закуски.\
Компания славится своей высокой скоростью обслуживания и качеством своей продукции.\
\n\nСейчас RZ FAST FOOD является одним из лидеров в индустрии быстрого питания.\
Компания имеет более 2000 ресторанов в разных странах мира,\
и продолжает активно развиваться и расширять свою сеть.\
\n\nКомпания RZ FAST FOOD также активно поддерживает благотворительные проекты\
и участвует в социально значимых мероприятиях,\
с целью внести вклад в развитие общества и улучшение качества жизни людей.'
    await bot.send_photo(photo=pic, chat_id=message.chat.id, caption=text)


@dp.message_handler(regexp='🛍 Заказать')
async def reaction_on_order(message: Message):
    await message.answer('Заберите свой заказ самостоятельно или выберите доставку',
                         reply_markup=generate_type_of_order())


@dp.message_handler(regexp='🚖 Доставка')
async def reaction_on_delivery(message: Message):
    await message.answer('Отправьте геолокацию или выберите адрес доставки',
                         reply_markup=generate_delivery())


@dp.message_handler(regexp='🏃🏻‍♂️ Самовывоз')
async def pickup_reaction(message: Message):
    await message.answer('Выберите филиал',
                         reply_markup=generate_filial())


@dp.message_handler(regexp='📍 Язык')
async def reaction_on_language(message: Message):
    await message.answer('Выберите язык',
                         reply_markup=generate_menu_language())


async def show_main_menu(message: Message):
    """
    Функция возврата на главное меню
    :param message:
    :return:
    """
    await message.answer('Главное меню',
                         reply_markup=generate_main_menu())


filial = [i[0] for i in db.get_filials_names()]


@dp.message_handler(lambda message: message.text in filial)
async def show_menu(message: Message):
    await message.answer('Выберите категорию',
                         reply_markup=generate_menu_categories())


filial_info = ['ℹ' + i[0] for i in db.get_filials_names()]


@dp.message_handler(lambda message: message.text in filial_info)
async def information_filial(message: Message):
    chat_id = message.chat.id
    malika = open('malika.jpg', mode='rb')
    chorsu = open('chorsu.jpg', mode='rb')
    maksimka = open('maksimka.jpg', mode='rb')
    chilanzar = open('chilanzar.jpg', mode='rb')

    mes = message.text
    mess = mes.split('ℹ')

    info = db.get_filial(mess[1])
    text = f'Название филиала: {info[1]}\nВремя работы: {info[3]}\nПосадочные места: {info[2]}\nЛокация: {info[4]}\n'
    filial_name = info[1]
    if filial_name == 'Чиланзар':
        await bot.send_photo(chat_id=chat_id, photo=chilanzar, caption=text)
    if filial_name == 'Малика':
        await bot.send_photo(chat_id=chat_id, photo=malika, caption=text)
    if filial_name == 'Максимка':
        await bot.send_photo(chat_id=chat_id, photo=maksimka, caption=text)
    if filial_name == 'Чорсу':
        await bot.send_photo(chat_id=chat_id, photo=chorsu, caption=text)


@dp.message_handler(regexp='🚩 К филиалам')
async def back_filial(message: Message):
    await message.answer('Выберите филиал',
                         reply_markup=generate_filial())


@dp.message_handler(regexp='⬅ Назад к доставке')
async def back_type_of_order(message: Message):
    await message.answer('Заберите свой заказ самостоятельно или выберите доставку',
                         reply_markup=generate_type_of_order())


@dp.message_handler(regexp='⬅ Назад к информации')
async def back_information(message: Message):
    await message.answer('Какую информацию вы хотите получить?', reply_markup=menu_information())


@dp.message_handler(regexp='⬅ Назад')
async def reaction_settings(message: Message):
    """
    Функционал кнопки назад
    :param message:
    :return:
    """
    await message.answer('Главное меню',
                         reply_markup=generate_main_menu())
