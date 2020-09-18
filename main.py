import config
import telebot
from datetime import datetime, timedelta


def day_and_week_file_read(flag):  # Функция для обработки дня и недели
    day = datetime.today()
    week = int(datetime.now().strftime("%V")) % 2  # 1 - чётная 0 - не чётная
    if flag:
        day = day + timedelta(days=1)
        if day.day % 7 == 0:
            week = (int(datetime.now().strftime("%V")) + 1) % 2  # 1 - чётная 0 - не чётная

    print(day.day, week)

    if week == 0:
        file_open = open('timetable/0/' + day.strftime('%A'), encoding='utf-8')
        file = file_open.read()

    elif week == 1:
        file_open = open('timetable/1/' + day.strftime('%A'), encoding='utf-8')
        file = file_open.read()

    file_open.close()
    return file


def calls():  # Функция для звоков
    file_open = open('timetable/calls', encoding='utf-8')
    file = file_open.read()
    file_open.close()
    return file


bot = telebot.TeleBot(config.token)  # Импортируе токе бота
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True, True, True,)  # Создаём клаву
keyboard1.row('сегодня', 'завтра', 'звонки', 'неделя')  # Присваиваем имена кнопок


@bot.message_handler(commands=['start'])  # При начале или команды /start
def start_message(message):  # Функция для отправки приветсвия
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=keyboard1)
    # Отправляем сообщение и показываем клаву


@bot.message_handler(commands=['help'])
def start_message(message):
    pass


@bot.message_handler(content_types=['text'])  # При любом сообщении
def send_text(message):
    if message.text.lower() == 'сегодня':  # Если в сообщение есть "сегодня" делаем
        flag = False

        bot.send_message(message.chat.id, 'Расписание на сегодня\n' + day_and_week_file_read(flag),
                         reply_markup=keyboard1)
    elif message.text.lower() == 'завтра':
        flag = True
        bot.send_message(message.chat.id, 'Расписание на завтра\n' + day_and_week_file_read(flag),
                         reply_markup=keyboard1)
    elif message.text.lower() == 'звонки':
        bot.send_message(message.chat.id, 'Расписание звонков\n' + calls(), reply_markup=keyboard1)
    elif message.text.lower() == 'неделя':
        number_week = int(datetime.now().strftime("%V")) - 35
        bot.send_message(message.chat.id, 'сейчас ' + str(number_week) + ' неделя.', reply_markup=keyboard1)
    else:
        bot.send_message(message.chat.id, 'Я не понял...', reply_markup=keyboard1)


bot.polling()  # звкрываем бота
