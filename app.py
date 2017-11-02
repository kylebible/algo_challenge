from flask import Flask, request, redirect, jsonify
import json
import os
from reddit_api import background_worker
from threading import Thread
from models import User, Team, Game, Challenge

app = Flask(__name__)


@app.route('/')
def index():
    return "Nothing to see here"


@app.route('/results', methods=['POST'])
def results():
    data = json.loads(request.form["payload"])
    # oid = data['value']['$oid']

    print("HALLELUJAH",data)

    return "hi"

@app.route('/slash', methods=['POST'])
def response():
    response_url = request.form.get("response_url")
    channel = request.form.get('channel_id')
    print(channel)
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