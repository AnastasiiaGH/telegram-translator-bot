import telebot
import deepl
from telebot import types

bot = telebot.TeleBot("5430029621:AAFg7L-o0ZnS-ZzEFkgfboWVCUlfirKC5Fc", parse_mode=None)
translator = deepl.Translator(auth_key="75f0db24-ae8f-fba4-79da-e82896e90bac:fx")


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "<b>Привет, бублик! "
                                      "Введи предложение на русском для перевода на английский</b>", parse_mode='html')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "/start - запуск бота\n/help - команды бота\n/translate_to - перевод на")


@bot.message_handler(commands=['translate_to'])
def translate_to(message):
    bot.send_message(message.chat.id, text="На какой язык нужно перевести?", reply_markup=set_buttons())


@bot.message_handler(content_types=['text'])
def set_buttons():
    markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton(text='English', callback_data='cd_English')
    button2 = types.InlineKeyboardButton(text='Russian', callback_data='cd_Russian')
    markup.add(button1)
    markup.add(button2)
    return markup


@bot.callback_query_handler(func=lambda call: True)
def answerEnglish(call):
    if call.data == 'cd_English':
        bot.send_message(call.chat.id, 'Translate to English enabled')
        translateEnglish()


@bot.callback_query_handler(func=lambda call: True)
def answerRussian(call):
    if call.data == 'cd_Russian':
        bot.send_message(call.chat.id, 'Translate to Russian enabled')
        translateRussian()


@bot.message_handler(content_types=['text'])
def translateEnglish(message):
    savedPhrase = message.text

    translateText = translator.translate_text(savedPhrase, target_lang="EN-US")
    bot.send_message(message.chat.id, str(translateText))


@bot.message_handler(content_types=['text'])
def translateRussian(message):
    savedPhrase = message.text

    translateText = translator.translate_text(savedPhrase, target_lang="RU")
    bot.send_message(message.chat.id, str(translateText))


bot.polling()
