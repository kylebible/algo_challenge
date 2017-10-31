from flask import Flask, request, redirect, send_from_directory
import json

app = Flask(__name__)


@app.route('/')
def index():
    return "Nothing to see here"


@app.route('/post_request', methods=['POST'])
def poll_answer():
    form_json = json.loads(request.form["payload"])
    print("HERE'S THE DATA", form_json)
    return "hi"

@app.route('/', defaults={'path': ''})  # Catch All urls, enabling copy-paste url
@app.route('/<path:path>')
def home(path):
    return redirect('/')

if __name__ == "__main__":
    app.run()