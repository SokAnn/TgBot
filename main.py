"""
Telegram Bot
description
"""

import telebot
from telebot import types
import config
import urllib.request

# Bot object
bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start_msg(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.username}!')
    bot.send_message(message.chat.id, 'Справка:\n\nДанный бот пишет какой тип контента ему прислал пользователь и пересылает его :)')


@bot.message_handler(commands=['help'])
def start_msg(message):
    bot.send_message(message.chat.id, 'Тут будет справка...')


@bot.message_handler(commands=['button'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Кнопка 1")
    item2 = types.KeyboardButton("Кнопка 2")

    markup.add(item1, item2)
    # bot.send_message(message.chat.id, parse_mode='html', reply_markup=markup)

#
# @bot.message_handler(content_types='text')
# def message_reply(message):
#     if message.text == "Кнопка 1":
#         bot.send_message(message.chat.id, "нажата кнопочка 1")
#     if message.text == "Кнопка 2":
#         bot.send_message(message.chat.id, "нажата кнопочка 2")


@bot.message_handler(content_types=['text', 'sticker', 'photo', 'audio', 'voice', 'document'])
def send_msg(message):
    if message.content_type == 'text':
        bot.send_message(message.chat.id, f"Вы прислали текст: \'{message.text}\'")
    if message.content_type == 'sticker':
        bot.send_message(message.chat.id, "Вы прислали стикер:")
        # bot.send_message(message.chat.id, message.sticker)  # sticker info
        bot.send_sticker(message.chat.id, message.sticker.file_id)
    if message.content_type == 'photo':
        bot.send_message(message.chat.id, "Вы прислали картинку:")
        # bot.send_message(message.chat.id, message)
    if message.content_type == 'audio':
        bot.send_message(message.chat.id, "Вы прислали аудио")
    if message.content_type == 'voice':
        bot.send_message(message.chat.id, "Вы прислали войс")
    if message.content_type == 'document':
        bot.send_message(message.chat.id, "Вы прислали документ")


bot.polling(none_stop=True)
