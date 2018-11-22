# DONT'T FORGET to import the required module in the child class

from linebot.models import TextSendMessage
from app.line import line_bot_api, line_handler

class BaseFeature:
    def simple_reply(self, event, message):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message)
        )

    def run(self, event):
        raise NotImplementedError