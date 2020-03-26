from flask import Flask, request, Response,url_for, render_template, redirect
from settings import TOKEN
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage
from viberbot.api.messages.keyboard_message import KeyboardMessage
from viberbot.api.viber_requests import ViberMessageRequest
from KEYBOARD import MAIN_KEYBOARD, ANSWER_KEYBOARD
from viberbot.api.viber_requests import ViberConversationStartedRequest

import random
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://jmltjbrbcabuar:f56c2482cf2dee0bd2bea44a1a622fdc30ceb0c0c1b81b207c0e98a565b89c06@ec2-54-247-118-139.eu-west-1.compute.amazonaws.com:5432/d1rt4olcajrbb2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


bot_config = BotConfiguration(
    name='weBoth',
    avatar='https://viber.com/avatar/jpg',
    auth_token=TOKEN
)
viber = Api(bot_config)
users = {}
import Classes as c

@app.route('/')
def index():  
    return render_template('index.html')

@app.route('/settings')
def settings():  
    s = c.mydb.get_settings()
    return render_template('settings.html', time=s.time, round = s.round, cwords=s.cwords)

@app.route("/sapply", methods=['POST'])
def set_settings():
    if request.method == 'POST':
        time = int(request.form.get('time'))
        round = int(request.form.get('round'))
        cwords = int(request.form.get('cwords'))

        c.mydb.set_settings(time, round, cwords)

    return redirect(url_for("settings"))

@app.route('/incoming', methods=['POST'])
def incoming():
    viber_request = viber.parse_request(request.get_data())
    message_proc(viber_request)
    return Response(status=200)


def message_proc(viber_request):
    if isinstance(viber_request, ViberConversationStartedRequest):
        text = "Этот бот для заучивания английских слов. Для начала введите start или нажмити кнопку снизу"
        viber.send_messages(viber_request.user.id, [TextMessage(text=text, keyboard=MAIN_KEYBOARD, tracking_data='tracking_data')])


    if isinstance(viber_request, ViberMessageRequest):
        user_id = viber_request.sender.id
        
        if not c.mydb.check_user(user_id):
            c.mydb.add_user(user_id)
     
        message = viber_request.message.text
        
        if message == "start" or message == "Давай начнем!" or message == 'S':
            print('start')
            new_user = c.User(user_id)
            users[new_user.id] = new_user

            users[user_id].get_question()     
            print(users[user_id].word) 
            for elem in  users[user_id].trans:
                print(elem)

            change_keyboard(user_id)
            send_message(user_id, users[user_id].word, ANSWER_KEYBOARD)
            return

        if message == "Привести пример":
            print('Пример')
            ex = users[user_id].get_rand_example()
            send_message(user_id, ex, ANSWER_KEYBOARD)
            return

        if message == "Отложить":
            c.mydb.update_answer_date(user_id)
            mess = 'Отложено'
            send_text_mess(user_id, mess)
            return
        
        if users.get(user_id) != None:
            print('Ответ')
            if message == users[user_id].trans[0]:
                print("OK")
                users[user_id].get_question()
                users[user_id].correct_ans()
                users[user_id].update_date()
                change_keyboard(user_id)
                next_or_result(user_id, "Верно")
                return
            else:
                print("NEOK")
                users[user_id].get_question()
                users[user_id].update_date()
                change_keyboard(user_id)
                next_or_result(user_id, "Не верно")
                return


answers_ind = [0, 1, 2, 3]


def next_or_result(id, text):
    s = c.mydb.get_settings()

    if users[id].quest_num == s.round + 1:
        send_result(id, text)
        return
    else:
        viber.send_messages(id, TextMessage(text=text))
        send_message(id, users[id].word, ANSWER_KEYBOARD)
        return


def send_result(id, text):
    s = c.mydb.get_settings()

    viber.send_messages(id, TextMessage(text=text))
    message = "Результат: " + str(users[id].correct) + "/" + str(s.round)
    viber.send_messages(id, TextMessage(text=message))
    info = c.mydb.get_user_info(id)
    message = "Выучено %d из %d \nПоследний опрос: %s" % info
    send_message(id, message, MAIN_KEYBOARD)
    users[id].reset()
    users.pop(id)
    return


def change_keyboard(id):
    answers = random.sample(answers_ind, len(answers_ind))
    for i in range(len(answers)):
        ANSWER_KEYBOARD["Buttons"][i]["Text"] = users[id].trans[answers[i]]
        ANSWER_KEYBOARD["Buttons"][i]["ActionBody"] = users[id].trans[answers[i]]


def send_message(id, text, keyb):
    text = TextMessage(text=text)
    keyboard = KeyboardMessage(tracking_data='tracking_data', keyboard=keyb)
    viber.send_messages(id, [text, keyboard])

def send_text_mess(id, text):
    text = TextMessage(text=text)
    viber.send_messages(id, text)



if __name__ == '__main__':
    app.run(port=80)

