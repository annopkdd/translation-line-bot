from flask import Flask, request, abort, jsonify
from googletrans import Translator
from firebase import firebase

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)


handler = WebhookHandler('bad655b08b23a1fac612c3875d672a70')
firebase = firebase.FirebaseApplication(
    'https://translation-line-bot.firebaseio.com/', None)


@app.route('/')
def index():
    return "<h1>Hello I'm fine!</h1>"


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api = LineBotApi(
        'TH51p3uJoggjsNFD+Jyfn1qMDac8XkB/8c3iyDubFdzOX89y5Xh3im85BjrQXJGjTCCdHUy/0WSKqGoDRe4CHECQXnjrE76WFRH1o0u9/0TZabB32vb/RjKuVumuUBbsVbMS8V6pXBDIXPxaonARSQdB04t89/1O/w1cDnyilFU=')
    translator = Translator()
    tran_word = 'Please Try Again'

    text_event_message = event.message.text
    lang_detect = translator.detect(text_event_message).lang
    print(lang_detect)

    if lang_detect == 'th':
        tran_word = translator.translate(
            text_event_message, dest='en').text
    elif lang_detect == 'en':
        tran_word = translator.translate(
            text_event_message, dest='th').text
    else:
        tran_word = 'Bot detect ' + lang_detect + ' language'

    text_message = TextSendMessage(
        text=tran_word)
    line_bot_api.reply_message(
        event.reply_token, text_message)


if __name__ == "__main__":
    app.run()
