import telebot
import requests
from bs4 import BeautifulSoup
from telebot import types
from parse import get_parse
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
        nominal_values = get_parse()
        for key, value in nominal_values.items():
            bot.send_message(call.message.chat.id, f"<i><b>{key}</b>: {value.text} сом</i>", parse_mode="HTML")
    if call.data == 'converter':
        currency_sum = bot.send_message(call.message.chat.id, 'Введите сумму:')
        bot.register_next_step_handler(currency_sum, choose_exchange)


def choose_exchange(message):
    global currency_sum
    currency_sum = message.text
    text_message = 'Выберите валюту: '
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("USD")
    btn2 = types.KeyboardButton("EUR")
    btn3 = types.KeyboardButton("KZT")
    btn4 = types.KeyboardButton("RUB")
    markup.add(btn1, btn2, btn3, btn4)
    nominal = bot.send_message(message.chat.id, text_message, reply_markup=markup)
    bot.register_next_step_handler(nominal, get_result)


def get_result(message):
    nominal = message.text
    current_rate = get_parse()
    if nominal == "USD":
        total_sum = float(currency_sum) * float(current_rate['USD'].text.replace(',', '.'))
    elif nominal == "EUR":
        total_sum = float(currency_sum) * float(current_rate['EUR'].text.replace(',', '.'))
    elif nominal == "KZT":
        total_sum = float(currency_sum) * float(current_rate['KZT'].text.replace(',', '.'))
    else:
        total_sum = float(currency_sum) * float(current_rate['RUB'].text.replace(',', '.'))
    bot.send_message(message.chat.id, f"{currency_sum} {nominal} = {round(total_sum, 2)} СОМ")


bot.polling()

