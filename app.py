import os
import json
import dice
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

    text = str(req['text']).lower()
    print(f'text: {text}')

    # every command is . prefixed ignore the rest
    if text[0] != '.':
        return "ok", 200
    # dont respond to bot messages
    if bot.sender_is_bot(req):
        return "ok", 200

    # split the message request by space
    command_lst = text.split(' ')
    print(f'list: {command_lst}')
    # remove period
    command = command_lst[0][1:]
    print(f'command: {command}')
    if command == 'help':
        bot.reply('go fuck yourself')
    if command == 'roll':
        bot.reply(roll_dice(command_lst))

    return "ok", 200

def roll_dice(command_lst):
    # second param is the dice
    dice_str = command_lst[1]
    print(f'dice string: {dice_str}')
    result = dice.roll(dice_str)
    print(f'result: {result}')
    if isinstance(result, list):
        total = sum(result)
        message = (
            f'Rolled {command_lst[1]} got result:\n'
            f'   {result}\n'
            f'Total: {total}'
        )
    else:
        message = (
            f'Rolled {command_lst[1]} got result:\n'
            f'   {result}'
        )

    return message

if __name__ == '__main__':
    print('Testing')
    msg = roll_dice(['roll', '2d6+5'])
    print(msg)
