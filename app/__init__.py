import os
import sys
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import requests
import datetime

channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

app = Flask(__name__)

app_settings = os.getenv(
    'APP_SETTINGS'
)
app.config.from_object(app_settings)

@app.route('/callback', methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        text = event.message.text.strip()
        if (text.startswith("today")):
            commands = text.split(' ')
            today = datetime.datetime.today()
            tomorrow = datetime.date.today() + datetime.timedelta(days=7)
            roomname = commands[1]
            payload = {
                "start": today.strftime("%Y-%m-%d"),
                "end": tomorrow.strftime("%Y-%m-%d")
            }
            url = 'http://reservasi.if.its.ac.id/calendar/accepted/%s' % roomname
            schedules = requests.get(url, payload)
            message = 'Kegiatan di %s untuk hari ini:' % roomname
            for schedule in schedules:
                messagePart = '\nAcara: %(title)s\nMulai: %(start)s\nSelesai: %(end)s\n' %{
                    'title': schedule['title'],
                    'start': schedule['start'],
                    'end':  schedule['end']
                }
                message += messagePart
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=message)
            )
    except Exception as error:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Error, silahkan cek ulang perintah anda")
        )
        print(error)
        pass

@app.route('/')
def hello():
    return "Hello there!"
