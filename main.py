"""
Telegram Bot
description
"""

import telebot
from telebot import types
import config
import cv2

# Bot object
bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start_msg(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.username}!')
    # send_sticker
    hi_sticker = open('stickers/yoda.tgs', 'rb')
    bot.send_sticker(message.chat.id, hi_sticker)
    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Справка")
    markup.add(item1)

    bot.send_message(message.chat.id,
                     'Данный бот пишет какой тип контента ему прислал пользователь и пересылает его обратно '
                     '(пока что, а дальше - лучше) :)',
                     reply_markup=markup)


@bot.message_handler(commands=['help'])
def help_msg(message):
    bot.send_message(message.chat.id, 'Тут будет справка...')


@bot.message_handler(commands=['button'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # keyboard
    item1 = types.KeyboardButton("Кнопка 1")
    # item2 = types.KeyboardButton("Кнопка 2")
    # markup.add(item1, item2)
    markup.add(item1)
    # bot.send_message(message.chat.id, parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text == "Справка":
        bot.send_message(message.chat.id, "Вы вызвали справку")


@bot.message_handler(content_types=['text', 'sticker', 'photo', 'audio', 'voice', 'document'])
def send_msg(message):
    if message.content_type == 'text':
        bot.send_message(message.chat.id, f"Вы прислали текст: \'{message.text}\'")
    if message.content_type == 'sticker':
        bot.send_message(message.chat.id, "Вы прислали стикер:")
        # message.sticker - sticker info
        bot.send_sticker(message.chat.id, message.sticker.file_id)
    if message.content_type == 'photo':
        bot.send_message(message.chat.id, "Вы прислали картинку:")
        # getting photo
        file = bot.get_file(message.photo[-1].file_id)
        download_file = bot.download_file(file.file_path)
        with open("photo.jpg", 'wb') as new_file:
            new_file.write(download_file)
        bot.reply_to(message, "Фото добавлено")
        # bot.send_photo(message.chat.id, message.photo[-1].file_id)

        # check face & save picture in DB
        num_faces = search_face("photo.jpg")
        bot.send_message(message.chat.id, f"Лиц обнаружено: {num_faces}")
        with open("photo.jpg", 'rb') as new_file:
            img = new_file.read()
            bot.send_photo(message.chat.id, img)



    if message.content_type == 'audio':
        bot.send_message(message.chat.id, "Вы прислали аудио")
        bot.send_audio(message.chat.id, message.audio.file_id)
    if message.content_type == 'voice':
        bot.send_message(message.chat.id, "Вы прислали войс:")
        bot.send_voice(message.chat.id, message.voice.file_id)
    if message.content_type == 'document':
        if message.document.file_name == 'mp4.mp4':
            bot.send_message(message.chat.id, "Вы прислали гифку:")
            bot.send_animation(message.chat.id, message.document.file_id)
        else:
            bot.send_message(message.chat.id, "Вы прислали документ")
            bot.send_document(message.chat.id, message.document.file_id)


def search_face(image):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    image = cv2.imread(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(10, 10)
    )
    if len(faces) > 0:
        # Рисуем квадраты вокруг лиц
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 0), 2)
        cv2.imwrite("photo.jpg", image)
        return len(faces)
    else:
        return 0


bot.polling(none_stop=True)
