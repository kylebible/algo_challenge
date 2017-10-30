from flask import Flask, request, redirect, send_from_directory
import json

app = Flask(__name__)


def create_app():

    @app.route('/get_all')
    def get_all():
        return "success"

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0')