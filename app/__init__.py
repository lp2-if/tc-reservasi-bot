import os
import traceback
from app.feature import feature_today
from app.line import line_bot_api, line_handler
from flask import Flask, request, abort
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)
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

@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        text = event.message.text.strip()
        if (text.lower().startswith("!today")):
            feature_today(event)
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
