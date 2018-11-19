import os
import requests
import datetime
import traceback
from pyquery import PyQuery as pq
from linebot.models import (
    TextSendMessage,
    CarouselTemplate, CarouselColumn, PostbackAction,
    MessageAction, TemplateSendMessage, URIAction
)
from app.line import line_bot_api, line_handler

class MessageEventHandler:
    def __init__(self):
        pass

    def handle(self, event):
        try:
            text = event.message.text.strip()

            if (text.lower().startswith("!today")):
                self.featureToday(event)
        except Exception as error:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Error, silahkan coba lagi")
            )
            print(str(error))
            traceback.print_exc()

    def featureToday(self, event):
        text = event.message.text.strip()
        commands = text.split(' ')
        today = datetime.datetime.today()
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)

        if (len(commands) == 1):
            self.send_room_list(event)
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

    def send_room_list(self, event):
        url = 'http://reservasi.if.its.ac.id/calendar'
        response = requests.get(url).content
        dom = pq(response)
        carousel_columns = []
        options = dom("#room_select option:not([selected])")
        actions = []
        for option in options:
            room_name = option.text
            actions.append(
                MessageAction(label='%s hari ini' % room_name, text='!today %s' % room_name)
            )
            if (len(actions) == 3):
                carousel_columns.append(
                    CarouselColumn(text="Daftar ruangan %s" % str(len(carousel_columns) + 1), actions=actions)
                )
                actions = []
        carousel_template = CarouselTemplate(
            columns=carousel_columns
        )
        template_message = TemplateSendMessage(
            alt_text='Daftar ruangan', template=carousel_template
        )
        line_bot_api.reply_message(event.reply_token, template_message)