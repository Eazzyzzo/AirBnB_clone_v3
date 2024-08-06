#!/usr/bin/python3
"""
Index module
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """
    Status route
    :return: JSON response indicating the status of the API
    """
    data = {
        "status": "OK"
    }
    resp = jsonify(data)
    resp.status_code = 200
    return resp


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def stats():
    """
    Stats route to get the count of all objects
    :return: JSON response with the count of all objects by type
    """
    data = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }
    resp = jsonify(data)
    resp.status_code = 200
    return resp
