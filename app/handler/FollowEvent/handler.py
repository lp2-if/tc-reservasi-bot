from app.line import line_bot_api, line_handler
from linebot.models import TextSendMessage

class FollowEventHandler:
    def __init__(self):
        pass

    def handle(self, event):
        user_id = event.source.user_id

        profile = line_bot_api.get_profile(user_id)

        firstName = profile.display_name.split(' ')[0]

        message = "Halo " + firstName + ", terima kasih sudah menambahkan saya sebagai teman.\nSaya dapat membantu anda terkait informasi reservasi ruangan di Departemen Informatika ITS."

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message)
        )