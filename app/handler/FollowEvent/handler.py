from app.line import line_bot_api, line_handler
from linebot.models import TextSendMessage
from app.utils import MessageFactory

class FollowEventHandler:
    def __init__(self):
        pass

    def handle(self, event):
        user_id = event.source.user_id

        profile = line_bot_api.get_profile(user_id)

        first_name = profile.display_name.split(' ')[0]

        message_body = MessageFactory.follow_message(first_name)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message_body)
        )
