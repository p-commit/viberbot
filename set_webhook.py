from settings import TOKEN, WEBHOOK
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration

bot_configuration = BotConfiguration(
    name='weBoth',
    avatar='weath.pythonanywhere.com',
    auth_token=TOKEN
)

viber = Api(bot_configuration)
viber.set_webhook(WEBHOOK)
