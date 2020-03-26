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
from models import Users, Settings
from apscheduler.schedulers.blocking import BlockingScheduler
import requests
from settings import WEBHOOK

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://jmltjbrbcabuar:f56c2482cf2dee0bd2bea44a1a622fdc30ceb0c0c1b81b207c0e98a565b89c06@ec2-54-247-118-139.eu-west-1.compute.amazonaws.com:5432/d1rt4olcajrbb2'
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


@sched.scheduled_job('interval', seconds= 30) 
def send_notification():

    headers = {
        'X-Viber-Auth-Token':'4ac8d8cbf4e7d1f9-24673fe4c1ca19ac-55268fef733cbeb', 
        'Content-Type':'application/json'
        }
    response = requests.post(WEBHOOK, headers=headers)

    users = db.session.query(Users)
    s = db.session.query(Settings).first()
   
    for elem in users:
        delta_time = dt.datetime.now() - elem.date
        delta_in_minutes = delta_time.days * 24 * 60 + delta_time.seconds / 60
        print(delta_in_minutes)

        # if delta_in_minutes < min:
        #     send_text_message(elem.user_id, "До уведомления еще " + str(min*60 - delta_in_minutes * 60) + " секунд")  
        
        if delta_in_minutes >=s.time:
            send_message(elem.user_id, "Вы давно не повторяли слова, желаете повторить?", NOTIFICATION_KEYBOARD)          
            
sched.start()