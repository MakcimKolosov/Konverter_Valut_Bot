
import telebot
import requests
import json
from config import keys, TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Это бот для конвертации валют. Формат команды:\n<имя валюты>\
<имя валюты для конвертации><количество>\
    Например: Евро Доллар 100\nСписок доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        quote, base, amount = message.text.split(' ')
        amount = float(amount)
    except ValueError:
        bot.reply_to(message, 'Ошибка: Неверный формат ввода.')
        return

    if quote not in keys or base not in keys:
        bot.reply_to(message, 'Ошибка: Неверная валюта. /values')
        return

    r = requests.get(f'https://v6.exchangerate-api.com/v6/bc671913bc5fa8fa2085c93e/pair/{keys[quote]}/{keys[base]}')
    response = json.loads(r.content)

    if 'result' in response and response['result'] == 'error':
        bot.reply_to(message, 'Ошибка: Неверные данные на сервере.')
        return

    total_base = response['conversion_rate'] * amount
    text = f'Цена {amount} {quote} в {base} - {total_base}'
    bot.send_message(message.chat.id, text)

bot.polling()

