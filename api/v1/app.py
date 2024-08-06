#!/usr/bin/python3
"""
app module
"""

from flask import Flask, jsonify
from flask_cors import CORS
from os import getenv

from api.v1.views import app_views
from models import storage


app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """
    Closes the storage on teardown
    :param exception: The exception that caused teardown
    """
    storage.close()


@app.errorhandler(404)
def handle_404(exception):
    """
    Handles 404 errors by returning a JSON response
    :param exception: The exception that caused the 404 error
    :return: JSON response with error message and 404 status code
    """
    data = {"error": "Not found"}
    resp = jsonify(data)
    resp.status_code = 404
    return resp


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")
    app.run(host=host, port=port)
