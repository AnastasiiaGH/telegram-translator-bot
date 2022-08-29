import telebot
import deepl
from telebot import types

bot = telebot.TeleBot("5430029621:AAFg7L-o0ZnS-ZzEFkgfboWVCUlfirKC5Fc", parse_mode=None)
translator = deepl.Translator(auth_key="75f0db24-ae8f-fba4-79da-e82896e90bac:fx")


@bot.message_handler(commands=['start'])
def set_buttons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button1 = types.KeyboardButton(text='English')
    button2 = types.KeyboardButton(text='French')
    markup.add(button1)
    markup.add(button2)
    bot.send_message(message.chat.id, text='<b>Привет, бублик! На какой язык нужно перевести?</b>', parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "/start - запуск бота\n/help - команды бота")


@bot.callback_query_handler(func=lambda call: True)
def answerEnglish(call):
    if call.data == "English":
        translateEnglish()
        bot.send_message(call.chat.id, 'Translate to English enabled')


@bot.message_handler(content_types=['text'])
def answerFrench(call, message):
    if call.text == "French":
        bot.send_message(call.chat.id, 'Перевод на французкий включен. Напиши предложение для перевода')
        savedPhrase = message.text()

        bot.register_next_step_handler(savedPhrase, translateFrench)
        
    
@bot.message_handler(content_types=['text'])
def translateFrench(message, savedPhrase=None):
    translateText = translator.translate_text(savedPhrase, target_lang="FR")
    bot.send_message(message.chat.id, str(translateText))



@bot.message_handler(content_types=['text'])
def translateEnglish(message):
    savedPhrase = message.text

    translateText = translator.translate_text(savedPhrase, target_lang="EN-US")
    bot.send_message(message.chat.id, str(translateText))


bot.polling()
