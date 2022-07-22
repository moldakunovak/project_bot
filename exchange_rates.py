import telebot
import requests
from bs4 import BeautifulSoup
from telebot import types
from parse import get_parse

from decouple import config

bot = telebot.TeleBot(config("BOT_TOKEN"))


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

