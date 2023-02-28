import telebot.types
from configs import TOKEN, keys
from extensions import Converter, ConvertionException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def show_help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите:\n\n' \
           '<Название валюты, цену которой Вы хотите узнать>'\
           '<Название валюты, в которой надо узнать цену первой валюты> '\
           '<Количество первой валюты>.\n\n' \
           'Например:   Доллар Рубль 1\n\n' \
           'Увидеть список доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def show_values(message: telebot.types.Message):
    text = f'Доступные валюты:\n'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.title().split()
        if len(values) != 3:
            raise ConvertionException('Неверно введены параметры.\n'
                                      'Помощь - /help')
        quote, base, amount = values
        total_base = Converter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {format(float(total_base) * float(amount), ".2f")}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
