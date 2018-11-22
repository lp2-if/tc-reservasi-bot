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
from app.handler.MessageEvent.Features.HelpFeature import HelpFeature
from app.handler.MessageEvent.Features.StatusFeature import StatusFeature

class MessageEventHandler:
    def __init__(self):
        self.feature_today = TodayFeature()
        self.feature_help = HelpFeature()
        self.feature_status = StatusFeature()

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
            self.feature_help.run(event)
        elif (text.startswith("!status")):
            self.feature_status.run(event)
        elif (text.startswith("!")):
            self.reply(event, MessageFactory.command_not_found_message())

    def reply(self, event, message):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message)
        )