import os
import requests
import datetime
import traceback
from pyquery import PyQuery as pq
from linebot.models import (
    TextSendMessage, ButtonsTemplate,
    CarouselTemplate, CarouselColumn, PostbackAction,
    MessageAction, TemplateSendMessage, URIAction
)
from app.line import line_bot_api, line_handler
from app.utils import MessageFactory

class MessageEventHandler:
    def __init__(self):
        pass

    def handle(self, event):
        try:
            self.parse_command(event)
        except Exception as error:
            self.reply(event, MessageFactory.error_message())

            print(str(error))
            traceback.print_exc()

    def parse_command(self, event):
        if (event.message.type != "text"): return

        text = event.message.text.strip().lower()

        if (text.startswith("!today")):
            self.feature_today(event)
        elif (text.startswith("!help")):
            self.feature_help(event)
        elif (text.startswith("!status")):
            self.feature_status(event)
        elif (text.startswith("!")):
            self.reply(event, MessageFactory.command_not_found_message())

    def reply(self, event, message):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message)
        )

    def feature_help(self, event):
        message = MessageFactory.help_message()
        
        text_message = TextSendMessage(text=message)

        user_id = event.source.user_id
        first_name = " "
        try:
            profile = line_bot_api.get_profile(user_id)
            first_name = profile.display_name.split(' ')[0]
        except Exception as e:
            pass

        carousel_template = CarouselTemplate(
            columns=[
                CarouselColumn(text="Daftar perintah 1", actions=[
                    MessageAction(label='Daftar ruangan', text='!today'),
                    MessageAction(label='Jadwal LP2 hari ini',
                                  text='!today LP2'),
                    # URIAction(label='Web reservasi IF',
                    #           uri='http://reservasi.if.its.ac.id/'),
                    MessageAction(label='Status reservasi',
                                  text='!status %s' % first_name),
                ])
            ]
        )
        template_message = TemplateSendMessage(
            alt_text="Carousel menu not supported", template=carousel_template)
        line_bot_api.reply_message(event.reply_token, [
            text_message,
            template_message
        ])

    def feature_status(self, event):
        text = event.message.text.strip()
        commands = text.split(' ')
        if (len(commands) == 1):
            self.reply(
                event, MessageFactory.status_command_invalid_message())
            return
        name = commands[1]
        payload = {
            "peminjam": name
        }
        url = "http://reservasi.if.its.ac.id/reserve/status"
        response = requests.get(url, payload).content
        dom = pq(response)
        statuses = dom(".responsive-table tbody tr")
        title_message = "Status reservasi untuk %s" % name
        message = ""
        for status in statuses:
            tr = pq(status)
            activity_issuer = tr.children("td")[1].text
            activity_name = tr.children("td")[2].text
            activity_status = tr.children("td")[4].text
            message += "%(name)s\n%(activity)s\n%(status)s\n\n" % {
                'name': activity_issuer,
                'activity': activity_name,
                'status': activity_status
            }
        if (len(message) == 0):
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(
                        text="Tidak ada reservasi dari %s" % name)
                ]
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text=title_message),
                    TextSendMessage(text=message.strip())
                ]
            )

    def feature_today(self, event):
        text = event.message.text.strip()
        commands = text.split(' ')
        today = datetime.datetime.today()
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)

        if (len(commands) == 1):
            self.send_room_list(event)
            return

        roomname = commands[1]

        if not(self.is_room_exists(roomname)):
            self.reply(event, MessageFactory.room_not_found_message(roomname))
            return

        payload = {
            "start": today.strftime("%Y-%m-%d"),
            "end": tomorrow.strftime("%Y-%m-%d")
        }

        url = 'http://reservasi.if.its.ac.id/calendar/accepted/%s' % roomname

        schedules = requests.get(url, payload).json()

        title_message = 'Kegiatan di %s untuk hari ini:' % roomname

        message = ''

        for schedule in schedules:
            messagePart = '%(title)s\n%(start)s - %(end)s\n\n' % {
                'title': schedule['title'],
                'start': schedule['start'].split(' ')[1],
                'end':  schedule['end'].split(' ')[1]
            }
            message += messagePart
            
        if (message == ''):
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(
                        text="Hari ini tidak ada kegiatan di %s" % roomname)
                ]
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text=title_message),
                    TextSendMessage(text=message.strip())
                ]
            )

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

