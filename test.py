import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_task.settings')
django.setup()

from ads.models import AdModel
import telebot
import re
from datetime import timedelta
from django.db.models import F

bot = telebot.TeleBot('')


@bot.message_handler(commands=['start'])
def start(message):
    keyboard1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard1.row('Добавить', 'Не добавлять')
    bot.send_message(message.chat.id, 'Привет!\n'
                                      'Добавить новое объявление ?', reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def choice(message):
    """Выбор: добавить объявление или нет"""

    if message.text.lower() == 'не добавлять' or message.text.lower() == 'нет' or message.text.lower() == 'no':
        bot.send_message(message.chat.id, f'Когда захотите добавить объявление нажмите на /start')
    elif message.text.lower() == 'добавить' or message.text.lower() == 'да' or message.text.lower() == 'yes':
        msg = bot.send_message(message.chat.id, 'Какое будет название у объявления ?')
        bot.register_next_step_handler(msg, creating_a_new_ad)


name_of_new_ad = []


def creating_a_new_ad(message):
    """Проверка корректности имени объявления"""

    if message.text == '/start':
        msg = bot.send_message(message.chat.id, 'Если вы хотите начать всё сначала, просто нажмите на /start ещё раз')
        bot.register_next_step_handler(msg, start)
    elif not re.findall(r'^[a-zа-яё]', message.text, re.IGNORECASE):
        msg = bot.send_message(message.chat.id, 'Не корректное название объявления, задайте имя объявлению ещё раз')
        bot.register_next_step_handler(msg, creating_a_new_ad)
    elif re.findall(r'^[a-zа-яё]', message.text, re.IGNORECASE):
        name_of_new_ad.append(message.text)
        bot.send_message(message.chat.id, f'Ваше объявление будет называться так:\n '
                                          f'"{message.text.capitalize()}".')
        msg = bot.send_message(message.chat.id, 'Укажите цену объявления в рублях')
        bot.register_next_step_handler(msg, price_indication)


price = []


def price_indication(message):
    """Проверка корректности цены объявления"""

    if message.text == '/start':
        msg = bot.send_message(message.chat.id, 'Если вы хотите начать всё сначала, просто нажмите на /start ещё раз')
        bot.register_next_step_handler(msg, start)
    elif '-' in message.text:
        msg = bot.send_message(message.chat.id, 'Цена должна быть положительным числом, введите ещё раз.')
        bot.register_next_step_handler(msg, price_indication)
    elif message.text.replace('.', '').isdigit():
        text = round(float(message.text.replace(',', '.')), 2) if ',' in message.text else round(float(message.text), 2)
        if text >= 0:
            bot.send_message(message.chat.id,
                             f'{name_of_new_ad[-1].capitalize()} будет стоить {text}')
            price.append(text)
            keyboard1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            keyboard1.row('Есть горячая цена', 'Нет горячей цены')
            msg = bot.send_message(message.chat.id, 'Есть ли горячая цена?', reply_markup=keyboard1)
            bot.register_next_step_handler(msg, choice_about_the_hot_price)
    else:
        msg = bot.send_message(message.chat.id, 'Цена должна быть числом, введите ещё раз.')
        bot.register_next_step_handler(msg, price_indication)


def choice_about_the_hot_price(message):
    """Выбор: добавить горячую цену или нет"""

    if message.text.lower() == 'нет горячей цены' or message.text.lower() == 'нет' or message.text.lower() == 'no':
        AdModel.objects.create(name=name_of_new_ad[0], price=price[0], hot_price=False)
        AdModel.objects.filter(name=name_of_new_ad[0]).update(
            disappear_at=(F('disappear_at') + timedelta(hours=1)))
        del name_of_new_ad[0]
        del price[0]

        bot.send_message(message.chat.id, f'Ваше объявление закреплено\n')
        bot.send_message(message.chat.id, 'Если хотите разместить ещё одно объявление,'
                                          ' просто нажмите на /start ещё раз')
    elif message.text.lower() == 'есть горячая цена' or message.text.lower() == 'да' or message.text.lower() == 'yes':
        msg = bot.send_message(message.chat.id, 'Укажите горячую цену')
        bot.register_next_step_handler(msg, hot_price)


@bot.message_handler(content_types=['text'])
def hot_price(message):
    """Проверка корректности горячей цены"""

    if message.text == '/start':
        msg = bot.send_message(message.chat.id, 'Если вы хотите начать всё сначала, просто нажмите на /start ещё раз')
        bot.register_next_step_handler(msg, start)
    elif '-' in message.text:
        msg = bot.send_message(message.chat.id, 'Цена должна быть положительным числом, введите ещё раз.')
        bot.register_next_step_handler(msg, hot_price)
    elif message.text.replace('.', '').isdigit():
        text = round(float(message.text.replace(',', '.')), 2) if ',' in message.text else round(float(message.text), 2)
        if text >= 0:
            AdModel.objects.create(name=name_of_new_ad[0], price=text, hot_price=True)
            AdModel.objects.filter(name=name_of_new_ad[0]).update(
                disappear_at=(F('disappear_at') + timedelta(minutes=5)))

            bot.send_message(message.chat.id,
                             f'{name_of_new_ad[0].capitalize()} будет стоить {text}')
            del name_of_new_ad[0]
            del price[0]

            bot.send_message(message.chat.id, 'Ваше объявление будет закреплено,'
                                              ' пока иной пользователь не даст горячую цену".')
            bot.send_message(message.chat.id, 'Если хотите разместить ещё одно объявление,'
                                              ' просто нажмите на /start ещё раз')
    else:
        msg = bot.send_message(message.chat.id, 'Цена должна быть числом, введите ещё раз.')
        bot.register_next_step_handler(msg, hot_price)

bot.polling()
