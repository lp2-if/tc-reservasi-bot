import os
import requests
import datetime
from app.line import line_bot_api
from linebot.models import (
    TextSendMessage,
    CarouselTemplate, CarouselColumn, PostbackAction,
    MessageAction, TemplateSendMessage, URIAction
)

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

def feature_today(event):
    text = event.message.text.strip()
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
        messagePart = '%(title)s\n%(start)s - %(end)s\n\n' %{
            'title': schedule['title'],
            'start': schedule['start'].split(' ')[1],
            'end':  schedule['end'].split(' ')[1]
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