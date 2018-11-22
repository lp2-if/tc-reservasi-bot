from linebot.models import (
    TextSendMessage, ButtonsTemplate,
    CarouselTemplate, CarouselColumn, PostbackAction,
    MessageAction, TemplateSendMessage, URIAction
)
from app.line import line_bot_api, line_handler
from app.handler.MessageEvent.Features.BaseFeature import BaseFeature
from app.utils import MessageFactory

class HelpFeature(BaseFeature):
    def __init__(self):
        pass

    def run(self, event):
        message = self.construct_reply_message()

        user_first_name = self.get_user_first_name(event.source.user_id)

        carousel_template = self.construct_carousel(user_first_name)

        template_message = TemplateSendMessage(
            alt_text="Carousel menu not supported", template=carousel_template)

        line_bot_api.reply_message(event.reply_token, [
            message,
            template_message
        ])

    def get_user_first_name(self, user_id):
        try:
            profile = line_bot_api.get_profile(user_id)
            first_name = profile.display_name.split(' ')[0]
        except Exception as e:
            pass

        return first_name

    def construct_reply_message(self):
        message = MessageFactory.help_message()

        return TextSendMessage(text=message)

    def construct_carousel(self, first_name):
        return CarouselTemplate(
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