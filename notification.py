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


@sched.scheduled_job('interval', minutes=1) 
def send_notification():
    users = db.session.query(Users)
    for elem in users:
        delta_time = dt.datetime.now() - elem.date
        delta_in_minutes = delta_time.days * 24 * 60 + delta_time.seconds // 60
        if delta_in_minutes > 1:
            send_message(elem.user_id, "Вы давно не повторяли слова, желаете повторить?", NOTIFICATION_KEYBOARD)