#!/usr/bin/python3
"""
Routes for handling Review objects and operations
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.review import Review


@app_views.route("/places/<place_id>/reviews",
                 methods=["GET"], strict_slashes=False)
def reviews_by_place(place_id):
    """
    Retrieves all Review objects by place
    :param place_id: Place object ID
    :return: JSON list of all Review objects
    for the specified place or 404 error if not found
    """
    place_obj = storage.get("Place", str(place_id))
    if place_obj is None:
        abort(404)

    review_list = [obj.to_json() for obj in place_obj.reviews]
    return jsonify(review_list)


@app_views.route("/places/<place_id>/reviews",
                 methods=["POST"], strict_slashes=False)
def review_create(place_id):
    """
    Creates a new Review object
    :param place_id: Place object ID
    :return: JSON of the newly created Review object
    with status code 201 or error codes 400/404
    """
    review_json = request.get_json(silent=True)
    if review_json is None:
        abort(400, 'Not a JSON')
    if not storage.get("Place", place_id):
        abort(404)
    if "user_id" not in review_json:
        abort(400, 'Missing user_id')
    if not storage.get("User", review_json["user_id"]):
        abort(404)
    if "text" not in review_json:
        abort(400, 'Missing text')

    review_json["place_id"] = place_id
    new_review = Review(**review_json)
    new_review.save()
    resp = jsonify(new_review.to_json())
    resp.status_code = 201
    return resp


@app_views.route("/reviews/<review_id>",
                 methods=["GET"], strict_slashes=False)
def review_by_id(review_id):
    """
    Retrieves a specific Review object by ID
    :param review_id: Review object ID
    :return: JSON of the Review object with
    the specified ID or 404 error if not found
    """
    fetched_obj = storage.get("Review", str(review_id))
    if fetched_obj is None:
        abort(404)
    return jsonify(fetched_obj.to_json())


@app_views.route("/reviews/<review_id>",
                 methods=["PUT"], strict_slashes=False)
def review_put(review_id):
    """
    Updates a specific Review object by ID
    :param review_id: Review object ID
    :return: JSON of the updated Review
    object or error codes 400/404
    """
    review_json = request.get_json(silent=True)
    if review_json is None:
        abort(400, 'Not a JSON')

    fetched_obj = storage.get("Review", str(review_id))
    if fetched_obj is None:
        abort(404)

    for key, val in review_json.items():
        if key not in ["id", "created_at", "updated_at",
                       "user_id", "place_id"]:
            setattr(fetched_obj, key, val)
    fetched_obj.save()
    return jsonify(fetched_obj.to_json())


@app_views.route("/reviews/<review_id>",
                 methods=["DELETE"], strict_slashes=False)
def review_delete_by_id(review_id):
    """
    Deletes a Review object by ID
    :param review_id: Review object ID
    :return: Empty JSON dictionary with
    status code 200 or 404 if not found
    """
    fetched_obj = storage.get("Review", str(review_id))
    if fetched_obj is None:
        abort(404)

    storage.delete(fetched_obj)
    storage.save()
    return jsonify({})
