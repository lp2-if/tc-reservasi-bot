from app.line import line_bot_api, line_handler
from linebot.models import TextSendMessage

class JoinEventHandler:
    def __init__(self):
        pass

    def handle(self, event):
        message = "Halo teman - teman semua,\n"
        message += "Terima kasih sudah mengundang saya ke grup ini,\n"
        message += "Kirimkan pesan !help untuk melihat perintah yang tersedia."
        message += "Have a nice and productive day :D"

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message)
        )