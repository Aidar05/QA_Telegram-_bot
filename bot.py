import telebot
from telebot import types
from flask import Flask, request, abort
import json
import urllib
from QA_data import QA_data


token = "myTokenAsdf"
bot = telebot.TeleBot(token, threaded=False)
bot.remove_webhook()
bot.set_webhook(url=f'https://bizarre1sorcerer.pythonanywhere.com/{token}')

app = Flask(__name__)
data = QA_data()


@app.route('/')
def hello():
    return "Телеграм бот для SAPEK"



@app.route("/" + token, methods=['POST'])
def webhook():
    print("POST request received")


    if request.headers.get('content-type') == 'application/json':
        print("request.headers.get('content-type') == 'application/json'")
        json_string = request.get_data().decode('utf-8')
        print(json_string)

        try:
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
        except json.decoder.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            print(f"json_string was: {json_string}")

        return ''
    else:
        print("error")
        abort(403)



@app.route('/site-map', methods=['GET'])
def site_map():
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = urllib.parse.unquote(f"{rule.rule}, {methods}, {rule.endpoint}")
        output.append(line)

    response_text = '\n'.join(sorted(output))
    return response_text

# В самом начале приветстие
@bot.message_handler(commands=["start"])
def welcome(message):
    welcomeText = f'''Здравствуйте {message.from_user.first_name} {message.from_user.last_name}!

Добро пожаловать на канал Союза Автомобильных Перевозчиков и Экспедиторов Казахстана (САПЭК).

Мы объединяемся в САПЭК, чтобы проще и быстрее решать проблемы отечественных перевозчиков
и экспедиторов на любом уровне и где бы вы ни находились!

САПЭК - это юридическая, информационная и консультационная поддержка, достоверная информация от первоисточника и надёжные проверенные партнёры для бизнеса любого уровня!

Введите команду /help для получения меню с категориями вопросов
'''

    bot.send_message(message.chat.id, welcomeText)


@bot.message_handler(commands=["help"])
def display_menu(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Раздел 1", callback_data='submenu1'))
    keyboard.add(types.InlineKeyboardButton("Раздел 2", callback_data='submenu2'))
    keyboard.add(types.InlineKeyboardButton("Раздел 3", callback_data='submenu3'))

    bot.send_message(message.chat.id, "Выберите раздел вопроса:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "submenu1":
        keyboard = types.InlineKeyboardMarkup()
        counter = 1

        for question in data.subMenuOne.keys():
            keyboard.add(types.InlineKeyboardButton(f"{counter}: {question}", callback_data=question))

            counter += 1

        keyboard.add(types.InlineKeyboardButton("< Назад", callback_data='main'))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                               text='Выбранный раздел: Раздел 1', reply_markup=keyboard)

    elif call.data == "submenu2":
        keyboard = types.InlineKeyboardMarkup()
        counter = 1

        for question in data.subMenuTwo.keys():
            keyboard.add(types.InlineKeyboardButton(f"{counter}: {question}", callback_data=question))

            counter += 1

        keyboard.add(types.InlineKeyboardButton("< Назад", callback_data='main'))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                               text='Выбранный раздел: Раздел 2', reply_markup=keyboard)

    elif call.data == "submenu3":
        keyboard = types.InlineKeyboardMarkup()
        counter = 1

        for question in data.subMenuThree.keys():
            keyboard.add(types.InlineKeyboardButton(f"{counter}: {question}", callback_data=question))

            counter += 1

        keyboard.add(types.InlineKeyboardButton("< Назад", callback_data='main'))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                               text='Выбранный раздел: Раздел 3', reply_markup=keyboard)

    elif call.data == "main":
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("Раздел 1", callback_data='submenu1'))
        keyboard.add(types.InlineKeyboardButton("Раздел 2", callback_data='submenu2'))
        keyboard.add(types.InlineKeyboardButton("Раздел 3", callback_data='submenu3'))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                               text='Выберите раздел вопроса:', reply_markup=keyboard)

    elif call.data in data.subMenuOne:
        bot.send_message(call.message.chat.id, f"Ответ: {data.subMenuOne[call.data]}")


    elif call.data in data.subMenuTwo:
        bot.send_message(call.message.chat.id, f"Ответ: {data.subMenuTwo[call.data]}")


    elif call.data in data.subMenuThree:
        bot.send_message(call.message.chat.id, f"Ответ: {data.subMenuThree[call.data]}")


if __name__ == '__main__':
    app.run(port='43345')