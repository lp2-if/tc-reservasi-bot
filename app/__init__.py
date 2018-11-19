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
    CarouselTemplate, CarouselColumn, PostbackAction,
    MessageAction, TemplateSendMessage, URIAction
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

def test_carousel(event):
    carousel_template = CarouselTemplate(columns=[
        CarouselColumn(text='hoge1', title='fuga1', actions=[
            URIAction(label='Go to line.me', uri='https://line.me'),
            PostbackAction(label='ping', data='ping')
        ]),
        CarouselColumn(text='hoge2', title='fuga2', actions=[
            PostbackAction(label='ping with text', data='ping', text='ping'),
            MessageAction(label='Translate Rice', text='米')
        ]),
    ])
    template_message = TemplateSendMessage(
        alt_text='Carousel alt text', template=carousel_template)
    line_bot_api.reply_message(event.reply_token, template_message)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        text = event.message.text.strip()
        if (text.lower().startswith("today")):
            commands = text.split(' ')
            today = datetime.datetime.today()
            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            if (len(commands) == 1):
                test_carousel(event)
                return
            roomname = commands[1]
            payload = {
                "start": today.strftime("%Y-%m-%d"),
                "end": tomorrow.strftime("%Y-%m-%d")
            }
            url = 'http://reservasi.if.its.ac.id/calendar/accepted/%s' % roomname
            schedules = requests.get(url, payload).json()
            titleMessage = 'Kegiatan di %s untuk hari ini:' % roomname
            message = ''
            for schedule in schedules:
                messagePart = 'Acara: %(title)s\nMulai: %(start)s\nSelesai: %(end)s\n\n' %{
                    'title': schedule['title'],
                    'start': schedule['start'],
                    'end':  schedule['end']
                }
                message += messagePart
            if (message == ''):
                line_bot_api.reply_message(
                    event.reply_token,
                    [
                        TextSendMessage(text="Hari ini tidak ada kegiatan di %s" %roomname)
                    ]
                )
            else :
                line_bot_api.reply_message(
                    event.reply_token,
                    [
                        TextSendMessage(text=titleMessage),
                        TextSendMessage(text=message)
                    ]
                )
    except Exception as error:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Error, silahkan cek ulang perintah anda")
        )
        print(error)

@app.route('/')
def hello():
    return "Hello there!"
