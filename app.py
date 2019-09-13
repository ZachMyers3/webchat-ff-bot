import os
import json
import dice
from flask import Flask, request
from groupme import GroupmeBot
import datetime

from ff_espn_api import League

app = Flask(__name__)
# groupme bot id
try:
    bot_id = os.environ["GROUPME_BOT_ID"]
except KeyError:
    print('GROUPME_BOT_ID environment variable not set, please set variable and re-run')
# espn ff league id
try:
    league_id = os.environ["ESPN_LEAGUE_ID"]
except KeyError:
    league_id = None
if league_id:
    league = League(league_id, int(datetime.datetime.now().strftime('%Y')))
else:
    league = None

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
    if command == 'matchups':
        bot.reply(league_matchups(command_lst))
    if command == 'scores':
        bot.reply(league_scoreboard(command_lst))
    if command == 'proj':
        bot.reply(league_projections(command_lst))

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

def league_matchups(command_lst):
    if not league:
        print('No league defined exiting')
        return
    scoreboard = league.scoreboard()
    scores = ['Matchups for this week:\n']
    max_size = 0
    for matchup in scoreboard:
        home_len = len(f'{matchup.home_team.team_name} ({matchup.home_team.wins}-{matchup.home_team.wins})')
        if home_len > max_size:
            max_size = home_len
    for matchup in scoreboard:
        home = f'{matchup.home_team.team_name} ({matchup.home_team.wins}-{matchup.home_team.wins})'.ljust(max_size)
        away = f'{matchup.away_team.team_name} ({matchup.away_team.wins}-{matchup.away_team.losses})'
        format_str = f'{home} vs {away}\n'
        scores.append(format_str)
    message = ''
    for msg_str in scores:
        message += msg_str

    return message

def league_scoreboard(command_lst):
    if not league:
        return
    # try and get week # from second arg
    try:
        week = int(command_lst[1])
        week_str = f'Week {week}'
    except:
        week = 0
        week_str = 'This Week'
    box_scores = league.box_scores(week)
    scores = [f'Scores for {week_str}:\n']
    max_size = 0
    for score in box_scores:
        home_len = len(f'{score.home_team.team_abbrev} {score.home_score:.2f}')
        if home_len > max_size:
            max_size = home_len
    for score in box_scores:
        home = f'{score.home_team.team_abbrev} {score.home_score:.2f}'.ljust(max_size)
        away = f'{score.away_score:.2f} {score.away_team.team_abbrev}'
        format_str = f'{home} - {away}\n'
        scores.append(format_str)
    message = ''
    for strings in scores:
        message += strings
    return message

def league_projections(command_lst):
    if not league:
        return
    # try and get week # from second arg
    try:
        week = int(command_lst[1])
        week_str = f'Week {week}'
    except:
        week = 0
        week_str = 'This Week'
    box_scores = league.box_scores(week)
    scores = [f'Projected Scores for {week_str}:\n']
    max_size = 0
    for score in box_scores:
        home_proj = get_projected_points(score.home_lineup)
        home_size = len(f'{score.home_team.team_abbrev} {home_proj:.2f}')
        if home_size > max_size:
            max_size = home_size
    for score in box_scores:
        home_proj = get_projected_points(score.home_lineup)
        away_proj = get_projected_points(score.away_lineup)
        home = f'{score.home_team.team_abbrev} {home_proj:.2f}'.ljust(max_size)
        away = f'{away_proj:.2f} {score.away_team.team_abbrev}'
        format_str = f'{home} - {away}\n'
        scores.append(format_str)
    message = ''
    for strings in scores:
        message += strings
    return message

def get_projected_points(lineup):
    total_proj = 0
    for player in lineup:
        if player.slot_position == 'BE':
            continue
        if player.points != 0:
            total_proj += player.points
        else:
            total_proj += player.projected_points

    return total_proj

def get_power_rankings(command_lst):
    if not league:
        return
    try:
        week = int(command_lst[1])
        week_str = f'Week {week}'
    except:
        week = 0
        week_str = 'This Week'
    rank_list = [f'Power Rankings for {week_str}:\n']
    ranks = league.power_rankings(week=week)
    for rank in ranks:
        rank_no = f'{float(rank[0]):.2f}'.ljust(5)
        rank_str = f'{rank_no} - {rank[1].team_name}\n'
        rank_list.append(rank_str)
    message = ''
    for rank_str in rank_list:
        message += rank_str

    return message


if __name__ == '__main__':
    print('Testing')
    msg = roll_dice(['roll', '2d6+5'])
    print(msg)
    print(league_matchups(['matchups']))
    print(league_scoreboard(['scoreboard', 'butt']))
    print(league_projections(['proj']))
    print(get_power_rankings(['ranks']))
