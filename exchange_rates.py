import telebot
import requests
from bs4 import BeautifulSoup
from telebot import types
from telebot.types import ReplyKeyboardMarkup
from decouple import config

bot = telebot.TeleBot(config("BOT_TOKEN"))

#
# @bot.message_handler(commands=["start", "привет"])
# def get_start_message(message):
#
#     text_message = f"Добро пожаловать {message.from_user.first_name} {message.from_user.last_name}!!!"
#     # bot.send_message(message.chat.id, text_message)
#     bot.reply_to(message, text_message)
#
#
# @bot.message_handler(content_types=['text'])
# def eho_message(message):
#     if message.text.lower() == "lang":
#         markup = types.InlineKeyboardMarkup(row_width=2)
#         btn1 = types.InlineKeyboardButton("Python", callback_data="py")
#         btn2 = types.InlineKeyboardButton("Java", callback_data="java")
#         btn3 = types.InlineKeyboardButton("JavaScript", callback_data="js")
#         btn4 = types.InlineKeyboardButton("Matlab", callback_data="mt")
#         btn5 = types.InlineKeyboardButton("Assembler", url="https://ru.wikipedia.org/wiki/%D0%90%D1%81%D1%81%D0%B5%D0%BC%D0%B1%D0%BB%D0%B5%D1%80")
#         markup.add(btn1, btn2, btn3, btn4,btn5)
#     # print(message.text)
#     mess = f"<i>Выберите язык \n<b>программирования</b>: </i>"
#     bot.send_message(message.chat.id, mess, parse_mode="HTML", reply_markup=markup)
#
# @bot.callback_query_handler(func=lambda call: True)
# def get_call_data(call):
#     if call.data == "py":
#         mess = "<a href='https://www.python.org/'>python</a>"
#         bot.send_message(call.message.chat.id, mess, parse_mode="HTML")
#     if call.data == "js":
#         mess = "<a href='hhttps://learn.javascript.ru/'>java</a>"
#         bot.send_message(call.message.chat.id, mess, parse_mode="HTML")
#     if call.data == "java":
#         mess = "<a href='https://www.java.com/ru/'>java</a>"
#         bot.send_message(call.message.chat.id, mess, parse_mode="HTML")
#     if call.data == "mt":
#         mess = "<a href='https://www.mathworks.com/products/matlab.html'>java</a>"
#         bot.send_message(call.message.chat.id, mess, parse_mode="HTML")
#
# # @bot.message_handler(content_types=['text'])
# # def get_markup(message):
# #     if message.text.lower() == "выбор":
# #         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
# #         btn1 =types.KeyboardButton("yes")
# #         btn2 =types.KeyboardButton("no")
# #         markup.add(btn1, btn2)
# #         bot.send_message(message.chat.id, "выберите:", reply_markup=markup)
#
# bot.polling()
#


@bot.message_handler(commands=["start", "привет"])
def get_start_message(message):
    text_message = f"Добро пожаловать {message.from_user.first_name} {message.from_user.last_name}!!!"
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("Актуальный курс валют", callback_data="actual_curs")
    btn2 = types.InlineKeyboardButton("Конвертер валют", callback_data='converter')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text_message, reply_markup=markup)




@bot.callback_query_handler(func=lambda call: True)
def get_call_data(call):
    if call.data == 'actual_curs':
        URL = 'https://www.nbkr.kg/XML/daily.xml'
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, 'xml')
        currency = soup.CurrencyRates.findAll('Currency')
        values = {'USD': currency[0].Value, 'EUR': currency[1].Value,
                  'KZT': currency[2].Value, 'RUB': currency[3].Value}
        for key, value in values.items():
            bot.send_message(call.message.chat.id, f"<i><b>{key}</b>: {value.text} сом</i>", parse_mode="HTML")
    elif call.data == 'converter':
        text_message = f"Выберите операцию:"
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton("Покупка", callback_data="buy")
        btn2 = types.InlineKeyboardButton("Продажа", callback_data='sell')
        markup.add(btn1, btn2)
        bot.send_message(call.message.chat.id, text_message, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'buy')
def send_all_genres(call):
    msg = bot.send_message(call.message.from_user.id, 'Введите сумму для покупки: ')
    bot.register_next_step_handler(msg, after_text_2)


def after_text_2(message):
    print('введённый пользователем номер телефона на шаге "смс":', message.text)


    # elif call.data == 'buy':
    #     text_message = f"Введите сумму для покупки:"
    #     markup = types.InlineKeyboardMarkup(row_width=2)
    #     btn1 = types.InlineKeyboardButton("USD", callback_data="buy_usd")
    #     btn2 = types.InlineKeyboardButton("EUR", callback_data='buy_eur')
    #     btn3 = types.InlineKeyboardButton("KZT", callback_data='buy_kzt')
    #     btn4 = types.InlineKeyboardButton("RUB", callback_data='buy_rub')
    #     markup.add(btn1, btn2, btn3, btn4)
    #     bot.send_message(call.message.chat.id, text_message, reply_markup=markup)











@bot.message_handler(content_types=['text'])
def eho_message(message):
    if message.text.lower() == "curs":
        # summa = float(input("введите сумму для конвертации: "))
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton("KGS", callback_data="KGS")
        btn2 = types.InlineKeyboardButton("USD", callback_data="USD")
        btn3 = types.InlineKeyboardButton("EUR", callback_data="EUR")
        btn4 = types.InlineKeyboardButton("RUB", callback_data="RUB")
        # btn5 = types.InlineKeyboardButton("Assembler", url="https://ru.wikipedia.org/wiki/%D0%90%D1%81%D1%81%D0%B5%D0%BC%D0%B1%D0%BB%D0%B5%D1%80")
        markup.add(btn1, btn2, btn3, btn4)
    # print(message.text)
        mess = f"<i><b>Выберите валюту </b>: </i>"
        bot.send_message(message.chat.id, mess, parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def get_call_data(call):
    if call.data == "KGS":
        mess = "<a href='https://www.nbkr.kg/XML/daily.xml'>KGS</a>"
        bot.send_message(call.message.chat.id, mess, parse_mode="HTML")
    if call.data == "USD":
        mess = "<a href='https://www.nbkr.kg/XML/daily.xml''>USD</a>"
        bot.send_message(call.message.chat.id, mess, parse_mode="HTML")
    if call.data == "EUR":
        mess = "<a href='https://www.nbkr.kg/XML/daily.xml''>EUR</a>"
        bot.send_message(call.message.chat.id, mess, parse_mode="HTML")
    if call.data == "RUB":
        mess = "<a href='https://www.nbkr.kg/XML/daily.xml''>RUB</a>"
        bot.send_message(call.message.chat.id, mess, parse_mode="HTML")

# @bot.message_handler(content_types=['text'])
# def get_markup(message):
#     if message.text.lower() == "выбор":
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         btn1 =types.KeyboardButton("yes")
#         btn2 =types.KeyboardButton("no")
#         markup.add(btn1, btn2)
#         bot.send_message(message.chat.id, "выберите:", reply_markup=markup)

bot.polling()

