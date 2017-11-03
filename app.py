from flask import Flask, request, redirect, jsonify
import json
import os
from reddit_api import background_worker, randomize_teams
from threading import Thread
from models import User, Team, Game, Challenge

app = Flask(__name__)

num_teams = int(os.environ['NUM_TEAMS'])
team_members = int(os.environ['NUM_MEMBERS'])

@app.route('/')
def index():
    return "Nothing to see here"


@app.route('/results', methods=['POST'])
def results():
    data = json.loads(request.form["payload"])
    game_id = data['callback_id']
    game = Game.objects.get(id=game_id)
    player_id = data['user']['id']
    player_name = data['user']['name']
    challenge_id = data['actions'][0]['value']
    try:
        player = User.objects.get(id=player_id)
    except:
        print("couldn't find player, making new one")
        player = User(id=player_id, username=player_name)
        player = player.save()
    
    challenge = Challenge.objects.get(id=challenge_id)
    for challenge in game.choices:
        if player in challenge.votes:
            return "You've already voted!"

    challenge.votes.append(player)
    challenge = challenge.save()
    game = Game.objects.get(id=game_id)

    players_voted = []
    for challenge in game.choices:
        players_voted += challenge.votes
    print("players voted", players_voted)
    if len(players_voted) >= team_members:
        teams = randomize_teams(players_voted, num_teams, game)
        message_str = "Everyone has voted and we have our teams!\n"
        team_no = 1
        for team in teams:
            message_str += "Team"+str(team_no)+"\n"
            team_no += 1
            for member in team:
                message_str += member.username+"\n"
            message_str += "\n"
        message = {
            "text": message_str
        }
        return message

    return "hi"

@app.route('/slash', methods=['POST'])
def response():
    response_url = request.form.get("response_url")
    channel = request.form.get('channel_id')
    thr = Thread(target=background_worker, args=[response_url, channel])
    thr.start()

    message = {
        "text": "Working on your request!"
    }

    return jsonify(message)
    # return

@app.route('/', defaults={'path': ''})  # Catch All urls, enabling copy-paste url
@app.route('/<path:path>')
def home(path):
    return redirect('/')

if __name__ == "__main__":
    app.run()