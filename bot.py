import telebot
import csv
from parsing import exchange_currency
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from text import text_start


TOKEN = ''

keyboard = InlineKeyboardMarkup()
# inline_1 = InlineKeyboardButton(text='Регистрация',callback_data='registration')
# inline_2 = InlineKeyboardButton(text='Button_2',callback_data='button2')
# inline_3 = InlineKeyboardButton(text='Фото',callback_data='photo')
inline_4 = InlineKeyboardButton(text='Рассылка',callback_data='mailing')
inline_5 = InlineKeyboardButton(text='Выборочная рассылка',callback_data='selective_mailing')
inline_6 = InlineKeyboardButton(text='Тех. поддержка',callback_data='support')
inline_7 = InlineKeyboardButton(text='Курсы валют',callback_data='exchange')
inline_8 = InlineKeyboardButton(text='Фото',callback_data='photo')
keyboard.row(inline_4,inline_5, inline_6, inline_7, inline_8)

list_1 = [1008889358, 5949761485, 5647517221, 5873445472,705754682,346706198]

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start','help'])
def hello_bot(message):
    with open('IDs.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        user_id = [str(message.from_user.id), str(message.from_user.first_name)]
        check_user = list(reader)
        if user_id not in check_user:
            with open('IDs.csv', 'a') as file:
                writer = csv.writer(file)
                writer.writerow([message.from_user.id, message.from_user.first_name])
                bot.send_message(message.from_user.id, text=text_start, reply_markup=keyboard)
        else:
            bot.send_message(message.from_user.id, text='Привет, ты есть в базе', reply_markup=keyboard)
    print(message.from_user.id,message.from_user.first_name)

# @bot.message_handler(commands=['start'])
# def start_func(message):
#     bot.send_message(chat_id=message.from_user.id, text='Hello!', reply_markup=keyboard)


@bot.callback_query_handler(lambda call: call.data == 'mailing')
def mainling(call):
    if call.from_user.id == 573015206:
        for item in list_1:
            try:
                bot.send_message(chat_id=item, text='Рассылка от Атоша')
            except Exception:
                continue

        bot.send_message(call.from_user.id, text='Рассылка успешно отправлена') 
    else:
        bot.send_message(call.from_user.id, text='Рассылка недоступна')

@bot.callback_query_handler(lambda call: call.data == 'selective_mailing')
def mainling(call):
    if call.from_user.id == 573015206:
        bot.answer_callback_query(call.id, 'Привет админ')
        # with open('database.txt','r') as file:
        #     display = file.read()
        #     bot.send_message(call.from_user.id, f'Все пользователи бота: \n\n{display}')  
        with open('IDs.csv','r', newline='', encoding='utf-8') as ids:
            reader = csv.reader(ids)
            for user_id, name in reader:
                bot.send_message(chat_id=user_id, text='Рассылка от Атоша')
    else:
        bot.reply_to(call, 'Вы не админ')



@bot.callback_query_handler(lambda call: call.data == 'exchange')
def exchange_cfunc(call):
    currency = exchange_currency()
    currency_list = []
    for key, value in currency.items():
        result = f'{key} - {value}'
        currency_list.append(result)
    text = '\n'.join(currency_list)
    bot.send_message(call.from_user.id, text=f'Курсы валют\n\n{text}')


@bot.callback_query_handler(lambda call: call.data == 'photo')
def photo_func(call):
    with open('4.jpg', 'rb') as img:
        bot.send_photo(call.from_user.id, img, caption = 'Photo')

@bot.callback_query_handler(lambda call: call.data == 'support')
def support_func(call):
    # Формируем ссылку на профиль пользователя
    user_id = call.from_user.id
    profile_link = f'tg://user?id={user_id}'

    # Формируем текст сообщения с ссылкой
    message_text = f'Привет, [{call.from_user.first_name}]({profile_link})'

    # Отправляем сообщение с ссылкой
    bot.send_message(call.from_user.id, text=message_text, parse_mode='MarkdownV2')

# @bot.callback_query_handler(lambda call: call.data == 'selective_mailing')
# def mainling(call):
#     if call.from_user.id == 573015206:
#         bot.answer_callback_query(call.id, 'Привет админ')
#         # with open('database.txt','r') as file:
#         #     display = file.read()
#         #     bot.send_message(call.from_user.id, f'Все пользователи бота: \n\n{display}')  
#         with open('IDs.csv','r', newline='', encoding='utf-8') as ids:
#             reader = csv.reader(ids)
#             for user_id, name in reader:
#                 bot.send_message(chat_id=user_id, text='Рассылка от Атоша')
#     else:
#         bot.reply_to(call, 'Вы не админ')


bot.polling(skip_pending=True)


