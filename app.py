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
    req = request.get_json()
    print(f'request: {req}')

    # every command is . prefixed ignore the rest
    if req.text[0] != '.':
        return "ok", 200
    # dont respond to bot messages
    if bot.sender_is_bot(req):
        return "ok", 200

    # split the message request by space
    command_lst = req.text.lower().split[' ']
    # remove period
    command = command_lst[0][1:]
    if command == 'help':
        bot.reply('go fuck yourself')

    return "ok", 200
