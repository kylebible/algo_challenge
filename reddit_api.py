import requests
import json
import re
from bson import json_util
import os
from models import User, Team, Game, Challenge

num_teams = os.environ['NUM_TEAMS']
team_members = os.environ['NUM_MEMBERS']


def get_random_post(requested_difficulty='Easy', any_difficulty=False):
    r = requests.get('http://reddit.com/r/dailyprogrammer/random.json', headers = {'User-agent': 'reddit_daily_algo_bot 0.1'})
    data = r.json()
    post = data[0]['data']['children'][0]['data']
    title = post['title']

    regex = r"\[[^)]+\].*?\[([^)]+)\]"
    try:
        difficulty = re.search(regex, title).group(1)
    except:
        return get_random_post(requested_difficulty)
        

    # if difficulty != requested_difficulty and not any_difficulty:
    #     print("wrong difficulty", difficulty)
    #     return get_random_post(requested_difficulty)
    
    description = post['selftext']
    description = description.replace('\n', '\\n')
    regex = r"^#(.*?)\\n#"
    try:
        description = re.search(regex, description).group(1)
    except:
        # print("regex failed for desc",post['selftext'])
        return get_random_post(requested_difficulty)
    
    description = description.replace('\\n', '\n')
    find_challenge = Challenge.objects(description=description)
    if len(find_challenge) > 0:
        return get_random_post(requested_difficulty)
    url = post['url']
    data = {
        'title': title,
        'description': description,
        'url': url,
        'difficulty': difficulty
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


def background_worker(response_url, channel):
    data = []
    for i in range(3):
        challenge = get_random_post(any_difficulty=True)
        new_challenge = Challenge(
            title=challenge['title'],
            description=challenge['description'],
            difficulty=challenge['difficulty'])
        data.append(new_challenge.save())
    game = Game(choices=data)
    game = game.save()
    message = {
        "text": "Here are three random Algorithm challenges!",
        "attachments": [{
            "title": data[0]["title"],
            "text": data[0]["difficulty"]+"\n"+data[0]["description"],
            "color": diff_color(data[0]["difficulty"])
        },
        {
            "title": data[1]["title"],
            "text": data[1]["difficulty"]+"\n"+data[1]["description"],
            "color": diff_color(data[1]["difficulty"])
        },
        {
            "title": data[2]["title"],
            "text": data[2]["difficulty"]+"\n"+data[2]["description"],
            "color": diff_color(data[2]["difficulty"])
        },
        {
            "title": "Choose which Algo you'd like to solve!",
            "callback_id": game.id,
            "attachment_type": "default",
            "actions": [
                {
                    "name": "choice",
                    "text": "Challenge #1",
                    "type": "button",
                    "value": data[0].id
                },
                {
                    "name": "choice",
                    "text": "Challenge #2",
                    "type": "button",
                    "value": data[1].id
                },
                {
                    "name": "choice",
                    "text": "Challenge #3",
                    "type": "button",
                    "value": data[2].id
                }
            ]
        }]
    }
    cleaned_message = json.loads(json_util.dumps(message))
    r = requests.post(response_url, data=json.dumps(cleaned_message))


if __name__ == "__main__":
    get_random_post()
