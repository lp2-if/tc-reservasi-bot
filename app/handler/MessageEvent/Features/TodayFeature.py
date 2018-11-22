import datetime
import requests
from app.utils.MessageFactory import MessageFactory
from linebot.models import (
    TextSendMessage, ButtonsTemplate,
    CarouselTemplate, CarouselColumn, PostbackAction,
    MessageAction, TemplateSendMessage, URIAction
)
from app.line import line_bot_api, line_handler
from app.handler.MessageEvent.Features.BaseFeature import BaseFeature
from pyquery import PyQuery as pq

class TodayFeature(BaseFeature):
    def init(self):
        self.calendar_base_endpoint = 'http://reservasi.if.its.ac.id/calendar/accepted/' 
        self.today_time = datetime.datetime.today()
        self.tomorrow_time = datetime.date.today() + datetime.timedelta(days=1)
    
    def run(self, event):
        commands = event.message.text.strip().split(' ')

        if (len(commands) == 1): 
            self.send_room_list(event)
            return
        else:
            if not(self.is_room_exists(commands[1])):
                self.simple_reply(event, MessageFactory.room_not_found_message(commands[1]))
                return

            room_schedules = self.get_room_schedule(event, commands[1])

            message = self.construct_message_body(room_schedules)

            self.send_room_schedules(event, message, commands[1])

    def send_room_schedules(self, event, message, roomname):
        if (message == ''):
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(
                        text="Hari ini tidak ada kegiatan di %s" % roomname)
                ]
            )
        else:
            title_message = 'Kegiatan di %s untuk hari ini:' % roomname
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text=title_message),
                    TextSendMessage(text=message.strip())
                ]
            )

    def get_room_schedule(self, event, roomname):
        payload = {
            "start" : self.today_time.strftime("%Y-%m-%d"),
            "end"   : self.tomorrow_time.strftime("%Y-%m-%d")
        }

        url = self.calendar_base_endpoint + roomname

        return self.hit_endpoint(url, payload)

    def construct_message_body(self, schedules):
        message = ''

        for schedule in schedules:
            messagePart = '%(title)s\n%(start)s - %(end)s\n\n' % {
                'title': schedule['title'],
                'start': schedule['start'].split(' ')[1],
                'end':  schedule['end'].split(' ')[1]
            }
            message += messagePart

        return message

    def hit_endpoint(self, url, payload):
        return requests.get(url, payload).json()

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
                MessageAction(label='%s hari ini' %
                              room_name, text='!today %s' % room_name)
            )
            if (len(actions) == 3):
                carousel_columns.append(
                    CarouselColumn(text="Daftar ruangan %s" % str(
                        len(carousel_columns) + 1), actions=actions)
                )
                actions = []
        carousel_template = CarouselTemplate(
            columns=carousel_columns
        )
        template_message = TemplateSendMessage(
            alt_text='Daftar ruangan', template=carousel_template
        )
        line_bot_api.reply_message(event.reply_token, template_message)

    def is_room_exists(self, roomname):
        exist_rooms = [
            'IF-101',
            'IF-102',
            'IF-103',
            'IF-104',
            'IF-105A',
            'IF-105B',
            'IF-106',
            'IF-108',
            'IF-111',
            'IF-112',
            'RAPAT1',
            'RAPAT2',
            'SIDANG',
            'AULA',
            'RTV',
            'LP1',
            'AJK',
            'LP2'
        ]

        return roomname in exist_rooms