from flask import Flask, request, redirect, jsonify
import json
import os
from reddit_api import background_worker, randomize_teams
from threading import Thread
from models import User, Team, Game, Challenge
import requests
from slackclient import SlackClient

app = Flask(__name__)

num_teams = int(os.environ['NUM_TEAMS'])
team_members = int(os.environ['NUM_MEMBERS'])
token = os.environ["SLACK_TOKEN"]

sc = SlackClient(token)

@app.route('/')
def index():
    return "Nothing to see here"


@app.route('/results', methods=['POST'])
def results():
    data = json.loads(request.form["payload"])
    channel = request.form.get('channel_id')
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
    most_votes = game.choices[0]
    for challenge in game.choices:
        players_voted += challenge.votes
        if len(most_votes.votes) < len(challenge.votes):
            most_votes = challenge
    if len(players_voted) >= team_members:
        game.challenge = most_votes
        game = game.save()
        teams = randomize_teams(players_voted, num_teams, game)
        message = {
            "replace_original": "false",
            "response_type": "in_channel",
            "text": "The votes are in! Today we are going to solve:\n"
            + "<" + game.challenge.url + "|"
            + game.challenge.title + ">",
            "attachments": []}
        team_no = 1
        for team in teams:
            team_attachment = {}
            team_attachment["title"] = "Team"+str(team_no)
            team_no += 1
            for member in team:
                # message_str += "<@"+member.id+">\n"
                message_str = "<@U7QL9HM50>\n"
            team_attachment["text"] = message_str
            message["attachments"].append(team_attachment)

        return jsonify(message)

    message = {
        "replace_original": "false",
        "text": "We've got your vote! Once the whole team's vote is in, I'll post the result!"
    }

    return jsonify(message)

    # sc.api_call(
    #     "chat.postMessage",
    #     channel=channel,
    #     text=
    # )

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

@app.route('/', defaults={'path': ''})  # Catch All urls, enabling copy-paste url
@app.route('/<path:path>')
def home(path):
    return redirect('/')

if __name__ == "__main__":
    app.run()