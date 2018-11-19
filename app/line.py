import os
from linebot import (
    LineBotApi, WebhookHandler
)

channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
line_bot_api = LineBotApi(channel_access_token)
line_handler = WebhookHandler(channel_secret)
