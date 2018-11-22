import requests
from pyquery import PyQuery as pq
from linebot.models import TextSendMessage
from app.line import line_bot_api, line_handler
from app.handler.MessageEvent.Features.BaseFeature import BaseFeature
from app.utils import MessageFactory

class StatusFeature(BaseFeature):
    def __init__(self):
        self.status_base_endpoint = "http://reservasi.if.its.ac.id/reserve/status"

    def run(self, event):
        commands = event.message.text.strip().split(' ')

        if (len(commands) < 2):
            self.simple_reply(
                event,
                MessageFactory.status_command_invalid_message()
            )

            return
        else:
            message = self.construct_status_message_body(commands[1])

            self.send_status(event, message, commands[1])

    def construct_status_message_body(self, name):
        response = self.hit_api(name)

        return self.parse_status_response(response)

    def parse_status_response(self, response):
        dom = pq(response)

        statuses = dom(".responsive-table tbody tr")

        message = ""

        for status in statuses:
            tr = pq(status)
            activity_issuer = tr.children("td")[1].text
            activity_name = tr.children("td")[2].text
            activity_status = tr.children("td")[4].text
            message += MessageFactory.status_message_body(activity_issuer, 
                                                          activity_name, 
                                                          activity_status)

        return message

    def hit_api(self, name):
        payload = {
            "peminjam" : name
        }

        return requests.get(self.status_base_endpoint, payload).content

    def send_status(self, event, message, name):
        if (len(message) == 0):
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(
                        text=MessageFactory.no_reservation_message(name))
                ]
            )
        else:
            title_message = MessageFactory.reservation_found_title_message(name)

            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text=title_message),
                    TextSendMessage(text=message.strip())
                ]
            )