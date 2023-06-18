import telebot
from telebot import types
import chat

bot=telebot.TeleBot("TOKEN")

try:
    from transformers import pipeline

    model = 'timpal0l/mdeberta-v3-base-squad2'

    qa_model = pipeline("question-answering", model=model)
except:
    qa_model=None

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id, "Привет! Напиши мне свой вопрос)")

@bot.message_handler(content_types=['text'])
def hz(msg):

    kr = ' в Кыргызской Республике'

    try:
        with open('data.txt') as f:
            lines = f.readlines()
    except:
        pass

    delete = types.ReplyKeyboardRemove()

    if msg.text == 'Простой':
        addition = '\nИспользуя как можно меньше терминов, по возможности меньше 5 предложений.'

        pred = chat.predict(lines[-1]+kr+addition)

        if len(pred) < 1e8:

            bot.send_message(msg.chat.id, pred+'\n\nМожете задать следующий вопрос.', reply_markup=delete)

        else:

            bot.send_message(msg.chat.id, qa_model(lines[-1], '')+'\n\nМожете задать следующий вопрос.', reply_markup=delete)

    elif msg.text == 'Подробный':
        addition = '\nОбъясни простыми словами, по возможности используй меньше 20 предложений.'

        pred = chat.predict(lines[-1]+kr+addition)

        if len(pred) < 1e9:

            bot.send_message(msg.chat.id, pred+'\n\nМожете задать следующий вопрос.', reply_markup=delete)

        else:

            bot.send_message(msg.chat.id, qa_model(lines[-1], '')+'\n\nМожете задать следующий вопрос.', reply_markup=delete)

    elif msg.text == 'Оффициальный':
        addition = ''

        pred = chat.predict(lines[-1]+kr+addition)

        if len(pred) < 1e10:

            bot.send_message(msg.chat.id, pred+'\n\nМожете задать следующий вопрос.', reply_markup=delete)

        else:

            bot.send_message(msg.chat.id, qa_model(lines[-1], '')+'\n\nМожете задать следующий вопрос.', reply_markup=delete)

    else:
        buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_1 = types.KeyboardButton("Простой")
        btn_2 = types.KeyboardButton("Подробный")
        btn_3 = types.KeyboardButton("Официальный")
        buttons.add(btn_1, btn_2, btn_3)
        bot.send_message(msg.chat.id, "Выберете уровень подробности ответа)", reply_markup=buttons)

        with open('data.txt', 'w') as f:
            f.write(msg.text)

bot.polling(none_stop=True)