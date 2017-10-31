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
        

    if difficulty != requested_difficulty and not any_difficulty:
        print("wrong difficulty", difficulty)
        return get_random_post(requested_difficulty)
    
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
        'url': url
    }
    return data



if __name__ == "__main__":
    get_random_post()
