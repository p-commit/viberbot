from flask import Flask, request, Response
from settings import TOKEN
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage
from viberbot.api.messages.keyboard_message import KeyboardMessage
from viberbot.api.viber_requests import ViberMessageRequest
from KEYBOARD import MAIN_KEYBOARD, ANSWER_KEYBOARD
from viberbot.api.viber_requests import ViberConversationStartedRequest
import random
from Classes import User, MyDB, db


app = Flask(__name__)
bot_config = BotConfiguration(
    name='weBoth',
    avatar='https://viber.com/avatar/jpg',
    auth_token=TOKEN
)
viber = Api(bot_config)
round = 5
users = {}



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

        if db.check_user(user_id):
            print("Пользователь уже существует")
        else:
            db.add_user(user_id)
            print("Пользователь добавлен")
 
        message = viber_request.message.text
        
        if message == "start" or message == "Давай начнем!":
            db.correct_answer(user_id, "спрашивать")
        #     new_user = User(user_id)
        #     users[new_user.id] = new_user
            
        #     users[user_id].get_question()          
        #     change_keyboard(user_id)
        #     send_message(user_id, users[user_id].word, ANSWER_KEYBOARD)
        #     return

        # if message == "Привести пример":
        #     ex = users[user_id].get_rand_example()
        #     send_message(user_id, ex, ANSWER_KEYBOARD)
        #     return

        # if message == users[user_id].trans[0]:
        #     users[user_id].get_question()
        #     users[user_id].correct += 1
        #     change_keyboard(user_id)
        #     next_or_result(user_id, "Верно")
        #     return
        # else:
        #     users[user_id].get_question()
        #     change_keyboard(user_id)
        #     next_or_result(user_id, "Не верно")
        #     return


answers_ind = [0, 1, 2, 3]


def next_or_result(id, text):
    if users[id].quest_num == round + 1:
        send_result(id, text)
    else:
        send_message(id, text+"\n" + users[id].word, ANSWER_KEYBOARD)


def send_result(id, text):
    message = text + "\nРезультат:" + str(users[id].correct) + "/" + str(round)
    users[id].reset()
    send_message(id, message, MAIN_KEYBOARD)


def change_keyboard(id):
    answers = random.sample(answers_ind, len(answers_ind))
    for i in range(len(answers)):
        ANSWER_KEYBOARD["Buttons"][i]["Text"] = users[id].trans[answers[i]]
        ANSWER_KEYBOARD["Buttons"][i]["ActionBody"] = users[id].trans[answers[i]]


def send_message(id, text, keyb):
    text = TextMessage(text=text)
    keyboard = KeyboardMessage(tracking_data='tracking_data', keyboard=keyb)
    viber.send_messages(id, [text, keyboard])


if __name__ == '__main__':
    app.run(port=80)