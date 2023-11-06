import telebot
from config import keys, TOKEN
from utils import ConvertionExeption, CryptoConverter

bot = telebot.TeleBot(TOKEN)

# создание исключения с названием ConversionExeption

# 1. инструкция для работы с ботом
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите комманду боту в следующем формате:\n‹имя валюты>\
<в какую валюту перевести>\
<количество переводимой валюты>\
Увидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


# 2. обработчик для работы с валютой
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


# 3. обработчик, который обрабатывает текст и возвращает курсы валют
@bot.message_handler(content_types=['text', ])

def convert(message: telebot.types.Message):
    #новый блок обработки для выявления ошибок (если введенных парметров больше 3, то ошибка)
    try:
        values = message.text.split(' ')
        if len(values) != 3:
           raise ConvertionExeption('Слишком много параметров')

        quote, base, amount = values
        total_base=CryptoConverter.convert(quote, base, amount)

    except ConvertionExeption as e:
        bot.reply_to(message, f'ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'не удалось обработать команду\n{e}')
    else:

        text = f'Цена {amount} {quote} - {total_base} {base}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)

