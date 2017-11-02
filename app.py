from flask import Flask, request, redirect, send_from_directory, jsonify
import json
from reddit_api import background_worker
from threading import Thread

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
    response_url = request.form.get("response_url")
    channel = request.form.get('channel')
    print(channel)
    thr = Thread(target=background_worker, args=[response_url])
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