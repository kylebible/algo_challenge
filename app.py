from flask import Flask, request, redirect, send_from_directory


app = Flask(__name__)


def create_app():
    @app.route('/')
    def index():
        return "Nothing to see here"


    @app.route('/post_request', methods=['POST'])
    def poll_answer():
        data = request.json
        print(data)
        return "hi"

    @app.route('/', defaults={'path': ''})  # Catch All urls, enabling copy-paste url
    @app.route('/<path:path>')
    def home(path):
        return redirect('/')
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0')