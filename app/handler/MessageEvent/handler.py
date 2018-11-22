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

from app.handler.MessageEvent.Features.TodayFeature import TodayFeature

class MessageEventHandler:
    def __init__(self):
        self.feature_today = TodayFeature()

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
            self.feature_today.run(event)
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