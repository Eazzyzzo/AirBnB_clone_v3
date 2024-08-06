#!/usr/bin/python3
"""
Routes for handling place and amenities linking
"""

from flask import jsonify, abort
from os import getenv
from api.v1.views import app_views
from models import storage


@app_views.route("/places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def amenity_by_place(place_id):
    """
    Retrieves all amenities of a place
    :param place_id: Place object ID
    :return: JSON list of all Amenity objects linked
    to the place or 404 error if not found
    """
    fetched_obj = storage.get("Place", str(place_id))
    if fetched_obj is None:
        abort(404)

    all_amenities = [obj.to_json() for obj in fetched_obj.amenities]
    return jsonify(all_amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def unlink_amenity_from_place(place_id, amenity_id):
    """
    Unlinks an amenity from a place
    :param place_id: Place object ID
    :param amenity_id: Amenity object ID
    :return: Empty JSON dictionary with status code 200 or 404 if not found
    """
    place_obj = storage.get("Place", str(place_id))
    amenity_obj = storage.get("Amenity", str(amenity_id))
    if not place_obj or not amenity_obj:
        abort(404)

    found = False
    for obj in place_obj.amenities:
        if str(obj.id) == amenity_id:
            if getenv("HBNB_TYPE_STORAGE") == "db":
                place_obj.amenities.remove(obj)
            else:
                place_obj.amenity_ids.remove(obj.id)
            place_obj.save()
            found = True
            break

    if not found:
        abort(404)

    resp = jsonify({})
    resp.status_code = 200
    return resp


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"], strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """
    Links an amenity with a place
    :param place_id: Place object ID
    :param amenity_id: Amenity object ID
    :return: JSON of the Amenity object added or error codes 400/404
    """
    place_obj = storage.get("Place", str(place_id))
    amenity_obj = storage.get("Amenity", str(amenity_id))
    if not place_obj or not amenity_obj:
        abort(404)

    if any(str(obj.id) == amenity_id for obj in place_obj.amenities):
        return jsonify(amenity_obj.to_json())

    if getenv("HBNB_TYPE_STORAGE") == "db":
        place_obj.amenities.append(amenity_obj)
    else:
        place_obj.amenities = amenity_obj
    place_obj.save()

    resp = jsonify(amenity_obj.to_json())
    resp.status_code = 201
    return resp
