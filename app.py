from flask import Flask, request, redirect, send_from_directory, jsonify
import json
from reddit_api import get_random_post

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
    data = get_random_post(any_difficulty=True)
    message = {
        'text': data['url'],
        'attachments': [{
            'text': data['description']
        }]
    }
    return jsonify(message)

@app.route('/', defaults={'path': ''})  # Catch All urls, enabling copy-paste url
@app.route('/<path:path>')
def home(path):
    return redirect('/')

if __name__ == "__main__":
    app.run()