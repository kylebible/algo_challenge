from flask import Flask, request, redirect, send_from_directory
import json

app = Flask(__name__)


@app.route('/')
def index():
    return "Nothing to see here"


@app.route('/response', methods=['POST'])
def response():
    data = json.loads(request.form["payload"])

    return "hi"

@app.route('/slash', methods=['POST'])
def response():
    return "This works!"

@app.route('/', defaults={'path': ''})  # Catch All urls, enabling copy-paste url
@app.route('/<path:path>')
def home(path):
    return redirect('/')

if __name__ == "__main__":
    app.run()