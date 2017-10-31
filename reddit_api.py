import requests
import json
import re


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


def background_worker(response_url):
    data = []
    for i in range(3):
        data.append(get_random_post(any_difficulty=True))
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
            "callback_id": "algo_choice",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "choice",
                    "text": "Challenge #1",
                    "type": "button",
                    "value": "challenge_1"
                },
                {
                    "name": "choice",
                    "text": "Challenge #2",
                    "type": "button",
                    "value": "challenge_2"
                },
                {
                    "name": "choice",
                    "text": "Challenge #3",
                    "type": "button",
                    "value": "challenge_3"
                }
            ]
        }]
    }
    r = requests.post(response_url, data=json.dumps(message))
    r = json.load(r)
    print("RESPONSE AFTER MESSAGE SENT", r)


if __name__ == "__main__":
    get_random_post()
