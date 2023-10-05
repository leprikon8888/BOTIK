import telebot
from telebot import types

token = '6559402688:AAEQi3czSbAc5SOQztaCvrAm8ctqf1pM2F0'

alex = telebot.TeleBot(token)

keyboard_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
tovar = types.KeyboardButton('Товари📋')
cart = types.KeyboardButton('Кошик🛒')
contacts = types.KeyboardButton('Контакти✉️')
keyboard_menu.add(tovar, cart, contacts)


@alex.message_handler(commands=['start'])
def start(message):
    alex.send_message(message.chat.id, 'Головне меню', reply_markup=keyboard_menu)
    new_order = open(f'orders/new_order_{message.chat.id}.txt', 'w')

    new_order.close()


@alex.message_handler(content_types=['text']) #вчимо Алекса обробляти текстові повідомлення
def menu_check(message): #Функція обробки
    # Умови
    if message.text == 'Товари📋':
        keyboard_category = types.ReplyKeyboardMarkup(resize_keyboard=True)
        phone = types.KeyboardButton('Телефони📱')
        tv = types.KeyboardButton('Телевізори📺')
        menu = types.KeyboardButton('↩️Меню')
        keyboard_category.add(phone, tv, menu)
        alex.send_message(message.chat.id, 'Оберіть категорію', reply_markup=keyboard_category)
    if message.text == 'Кошик🛒':
        file_cart = open(f'orders/new_order_{message.chat.id}.txt', 'r')
        cart = file_cart.read().split('\n')
        file_cart.close()
        message_text = ''
        total_price = 0
        for element in cart:
            if element:
                text_pars = element.split(';')
                total_price += int(text_pars[2].replace('$', '')) #додаємо до загальноі суми вартість товару
                message_text = message_text + f'{text_pars[0]} - {text_pars[1]}, ціна: {text_pars[2]}\n' #гарно виводимо дані у текст повідомлення
        message_text = message_text + f'Загальна сума - {total_price}$'
        orders_keyboard = types.InlineKeyboardMarkup()
        orders_button = types.InlineKeyboardButton(text='Оформити замовлення', callback_data='Оформити')
        orders_keyboard.add(orders_button)
        text_null = 'Кошик порожній, наповни його та оформлюй замовлення'
        if total_price:
            alex.send_message(message.chat.id, message_text, reply_markup=orders_keyboard)
        else:
            alex.send_message(message.chat.id, text_null)
    if message.text == 'Контакти✉️':
        alex.send_message(message.chat.id, 'https://instagram.com/so_sweet_lingerie?igshid=MWZjMTM2ODFkZg== \nнаш телефон/вайбер/телеграм +380637769743')
    if message.text == '↩️Меню':
        alex.send_message(message.chat.id, '🔝Меню', reply_markup=keyboard_menu)
    if message.text == 'Телефони📱':
        file_phone = open('phone.txt', 'r')
        db_phone = file_phone.read().split('\n')
        file_phone.close()
        phone_keyboard = types.InlineKeyboardMarkup()
        for schumacher in db_phone:
            if schumacher:
                text_pars = schumacher.split(';')
                button = types.InlineKeyboardButton(text=f'{text_pars[0]} - {text_pars[1]}, ціна: {text_pars[2]}', callback_data=schumacher)
                phone_keyboard.add(button)
        alex.send_message(message.chat.id, 'Категорія телефони📱:', reply_markup=phone_keyboard)
    if message.text == 'Телевізори📺':
        file_tv = open('tv.txt', 'r')
        db_tv = file_tv.read().split('\n')
        file_tv.close()
        tv_keyboard = types.InlineKeyboardMarkup()
        for el in db_tv:
            text_pars = el.split(';')
            button = types.InlineKeyboardButton(text=f'{text_pars[0]} - {text_pars[1]}дюймів, ціна: {text_pars[2]}', callback_data=el)
            tv_keyboard.add(button)
        alex.send_message(message.chat.id, 'Категорія телевізори📺:', reply_markup=tv_keyboard)


@alex.callback_query_handler(func=lambda call: True)
def call_data_me(call):
    if call.data:
        if call.data == "Оформити":
            user_number = alex.send_message(call.message.chat.id, "Напишіть номер телефону, та наш менеджер зв'яжеться з вами протягом 5 хвилин")
            alex.register_next_step_handler(user_number, check_order)
        else:
            new_order = open(f'orders/new_order_{call.message.chat.id}.txt', 'a')
            new_order.write(call.data + '\n')
            new_order.close()
            text_pars = call.data.split(';')
            alex.send_message(call.message.chat.id, f'{text_pars[0]} - {text_pars[1]} додано до кошика!')


def check_order(message):
    file_cart = open(f'orders/new_order_{message.chat.id}.txt', 'r')
    cart = file_cart.read().split('\n')
    file_cart.close()
    message_text2 = ''
    total_price = 0
    for element in cart:
        if element:
            text_pars = element.split(';')
            total_price += int(text_pars[2].replace('$', '')) #додаємо до загальної суми вартість товару
            message_text2 += f'{text_pars[0]} - {text_pars[1]}, ціна: {text_pars[2]}\n' #гарно виводимо дані у текст повідомлення
    message_text2 += f'\nЗагальна сума - {total_price}$\n'
    alex.send_message(-4036524456, f'Нове замовлення. \n{message_text2}\nНомер телефону; {message.text}')

alex.polling(none_stop=True, interval=0)
