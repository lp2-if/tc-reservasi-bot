import os
import traceback
from app.line import line_bot_api, line_handler
from flask import Flask, request, abort
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from app.handler.handler import Handler

app = Flask(__name__)
message_type_handler = Handler()
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
    app.logger.info("Request body: %s" % body)

    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@line_handler.default()
def handle_message(event):
    try:
        message_type_handler.handle(event)
    except Exception as error:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Error, silahkan coba lagi")
        )
        print(str(error))
        traceback.print_exc()

@app.route('/')
def hello():
    return "Hello there!"
