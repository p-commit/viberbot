from flask import Flask, request, Response
from settings import TOKEN
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage
from viberbot.api.messages.keyboard_message import KeyboardMessage
from viberbot.api.viber_requests import ViberMessageRequest
from KEYBOARD import NOTIFICATION_KEYBOARD
from viberbot.api.viber_requests import ViberConversationStartedRequest
import datetime as dt
from flask_sqlalchemy import SQLAlchemy
from models import Users
from apscheduler.schedulers.blocking import BlockingScheduler

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
sched = BlockingScheduler()
db = SQLAlchemy(app)

bot_config = BotConfiguration(
    name='weBoth',
    avatar='https://viber.com/avatar/jpg',
    auth_token=TOKEN
)
viber = Api(bot_config)


def send_message(id, text, keyb):
    text = TextMessage(text=text)
    keyboard = KeyboardMessage(tracking_data='tracking_data', keyboard=keyb)
    viber.send_messages(id, [text, keyboard])

def send_text_message(id, text):
    text = TextMessage(text=text)
    viber.send_messages(id, text)


@sched.scheduled_job('interval', seconds= 10) 
def send_notification():
   
    min = 1
    users = db.session.query(Users)
   
    for elem in users:
        delta_time = dt.datetime.now() - elem.date
        delta_in_minutes = delta_time.days * 24 * 60 + delta_time.seconds / 60
        print(delta_in_minutes)

        if delta_in_minutes < min:
            send_text_message(elem.user_id, "До уведомления еще " + str(min*60 - delta_in_minutes * 60) + " секунд")  
        else:
            send_message(elem.user_id, "Вы давно не повторяли слова, желаете повторить?", NOTIFICATION_KEYBOARD)          
            
sched.start()