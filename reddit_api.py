import requests
import json
import re
from random import randint
from bson import json_util
import os
from models import User, Team, Game, Challenge
from datetime import datetime
from random import shuffle
from slackclient import SlackClient

num_teams = int(os.environ['NUM_TEAMS'])
team_members = int(os.environ['NUM_MEMBERS'])
token = os.environ["SLACK_TOKEN"]

sc = SlackClient(token)


def get_reddit_post(url):
    r = requests.get(
        url+'.json',
        headers={
            'User-agent': 'reddit_daily_algo_bot 0.1'
        })
    data = r.json()
    post = data[0]['data']['children'][0]['data']
    title = post['title']

    description = post['selftext']
    description = description.replace('\n', '\\n')
    regex = r"^#(.*?)\\n#"
    try:
        description = re.search(regex, description).group(1)
    except:
        # print("regex failed for desc",post['selftext'])
        return "Couldn't parse out the description"

    description = description.replace('\\n', '\n')
    try:
        Challenge.objects.get(url=url, selected=True)
        print("challenge already exists")
        return "This already exists, submit a new one"
    except:
        pass

    url = post['url']
    data = {
        'title': title,
        'description': description,
        'url': url
    }
    return data


def diff_color(diff):
    if diff == "Hard":
        return "#CB3535"
    elif diff == "Intermediate":
        return "#E7AB17"
    elif diff == "Easy":
        return "#54D600"
    else:
        return "#2E5DFF"


def challenge_creation(response_url, channel, url):
    print("entered challenge creation")
    challenge = get_reddit_post(url)
    print("exited reddit post", challenge)
    new_challenge = Challenge(
        title=challenge['title'],
        description=challenge['description'],
        url=challenge['url'])
    new_challenge = new_challenge.save()
    game = Game.objects.get(active=True)
    game.submissions.append(new_challenge)
    game.save()
    message = {
        "text": "Great Choice! We'll let you know if it will be voted on when the challenge starts tomorrow!",
    }
    sc.api_call(
        "chat.postMessage",
        channel=channel,
        text=message["text"])


def choices_creation(response_url, channel, url):
    challenges = get_random_challenges()
    # TODO: make get_random_challenges()
    game = Game.objects.get(active=True)
    game.choices = challenges
    game = game.save()
    game_id = json.loads(json_util.dumps(game.id))
    message = {
        "response_type": "in_channel",
        "text": "Here are three Algorithm challenges!",
        "attachments": []
    }
    choices = {
        "title": "Choose which Algo you'd like to solve!",
        "callback_id": game_id['$oid'],
        "attachment_type": "default",
        "actions": []
    }
    for i, chall in enumerate(challenges):
        challenge_attachment = {}
        challenge_attachment[
            "title"] = "<" + chall.url + "|" + chall.title + ">"
        challenge_attachment["text"] = chall.description
        challenge_attachment["color"] = rand_color()
        # TODO: make rand_color()
        message["attachments"].append(challenge_attachment)
        choice = {}
        choice["name"] = "choice"
        choice["text"] = "Challenge #" + str(i + 1)
        choice["type"] = "button"
        choice["value"] = json.loads(json_util.dumps(chall.id))["$oid"]
        choices["actions"].append(choice)
    message["attachments"].append(choices)

    sc.api_call(
        "chat.postMessage",
        channel=channel,
        text=message["text"],
        response_type=message["response_type"],
        attachments=message["attachments"])


def get_random_challenges():
    game = Game.objects.get(active=True)
    submissions = game.submissions
    for _ in range(3):
        i = randint(0, len(submissions)-1)
        game.choices.append(submissions[i])
        del submissions[i]
    game.save()
    return game.submissions


def randomize_teams(names, no_teams, game):
    teams = []
    shuffle(names)
    for _ in range(no_teams):
        teams.append([])

    last_game = Game.objects.first()
    last = last_game.teams

    while names:
        for team in teams:
            if names:
                team.append(names.pop())

    for team in teams:
        if team in last:
            return randomize_teams(names, no_teams, game)

    teams_object = []
    for team in teams:
        max_driver_time = datetime.now()
        current_driver = ""
        for (idx, member) in enumerate(team):
            if 'last_lead' in member:
                if member.last_lead < max_driver_time:
                    max_driver_time = member.last_lead
                    current_driver = idx
            else:
                current_driver = idx
                break
        temp = team[0]
        team[0] = team[current_driver]
        team[current_driver] = temp
        team[0].last_lead = datetime.now()
        team[0].save()
        team = Team(members=team)
        teams_object.append(team)

    print(teams, teams_object)
    game.teams = teams_object
    game.save()

    return teams


if __name__ == "__main__":
    get_random_post()
