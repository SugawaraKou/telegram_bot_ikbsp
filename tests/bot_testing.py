import config
import telebot

bot = telebot.TeleBot(config.token)

# keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True, True, True)
# keyboard1.row('сегодня', 'завтра', 'звонки', 'неделя')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')


@bot.message_handler(commands=['art'])
def images(message):
    bot.send_photo(message.chat.id, photo=open('images/1.jpg', 'rb'))


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'Привет как сам?':
        bot.send_message(message.chat.id, 'хорошо')
    else:
        bot.send_message(message.chat.id, 'Я не понял...')


# @bot.message_handler(content_types=['sticker'])
# def sticker_id(message):
#     print(message)


bot.polling()
