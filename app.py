from flask import Flask, request, redirect, send_from_directory, jsonify
import json
from reddit_api import get_random_post, diff_color

app = Flask(__name__)


@app.route('/')
def index():
    return "Nothing to see here"


@app.route('/results', methods=['POST'])
def results():
    data = json.loads(request.form["payload"])

    return "hi"

@app.route('/slash', methods=['POST'])
def response():
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
    return jsonify(message)

@app.route('/', defaults={'path': ''})  # Catch All urls, enabling copy-paste url
@app.route('/<path:path>')
def home(path):
    return redirect('/')

if __name__ == "__main__":
    app.run()