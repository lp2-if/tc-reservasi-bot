from app.line import line_bot_api, line_handler
from linebot.models import TextSendMessage
from app.utils import MessageFactory

class JoinEventHandler:
    def __init__(self):
        pass

    def handle(self, event):
        message = MessageFactory.join_message()

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message)
        )
