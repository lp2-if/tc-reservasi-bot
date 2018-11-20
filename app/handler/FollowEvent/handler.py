from app.line import line_bot_api, line_handler
from linebot.models import TextSendMessage


class FollowEventHandler:
    def __init__(self):
        pass

    def handle(self, event):
        user_id = event.source.user_id

        profile = line_bot_api.get_profile(user_id)

        firstName = profile.display_name.split(' ')[0]

        message1 = "Halo " + firstName + \
            ", terima kasih sudah menambahkan saya sebagai teman.\nSaya dapat membantu anda terkait informasi reservasi ruangan di Departemen Informatika ITS.\n\n"

        message2 = "Beberapa perintah yang dapat kamu berikan: \n\n"

        command_msg = "1. !today\nUntuk melihat ruangan yang tersedia\n"
        command_msg += "2. !today <nama_ruang>\nUntuk melihat jadwal kegiatan di ruangan tersebut untuk hari ini\n"
        command_msg += "3. !status <nama_kamu>\nUntuk mengecek status reservasi kamu\n\n"
        command_msg += "4. !help\nUntuk mengetahui perintah yang tersedia\n\n"
        command_msg += "Hubungi admin LP2 untuk tambahan fitur"

        message_body = message1 + message2 + command_msg

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message_body)
        )
