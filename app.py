import os
import json
from flask import Flask, request
from groupme import GroupmeBot

app = Flask(__name__)
try:
    bot_id = os.environ["GROUPME_BOT_ID"]
except KeyError:
    print('GROUPME_BOT_ID environment variable not set, please set variable and re-run')

bot = GroupmeBot(bot_id)

# Called whenever the app's callback URL receives a POST request
# That'll happen every time a message is sent in the group
@app.route('/', methods=['POST'])
def webhook():
    # 'message' is an object that represents a single GroupMe message.
    message = request.get_json()
    print(f'message: {message}')

    # TODO: Your bot's logic here

    return "ok", 200
