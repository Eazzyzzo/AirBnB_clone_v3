#!/usr/bin/python3
"""
Routes for handling State objects and operations
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def state_get_all():
    """
    Retrieves all State objects
    :return: JSON list of all State objects
    """
    state_list = [obj.to_json() for obj in storage.all("State").values()]
    return jsonify(state_list)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def state_create():
    """
    Creates a new State object
    :return: JSON of the newly created State object
    with status code 201 or error codes 400
    """
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, 'Not a JSON')
    if "name" not in state_json:
        abort(400, 'Missing name')

    new_state = State(**state_json)
    new_state.save()
    resp = jsonify(new_state.to_json())
    resp.status_code = 201
    return resp


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def state_by_id(state_id):
    """
    Retrieves a specific State object by ID
    :param state_id: State object ID
    :return: JSON of the State object with
    the specified ID or 404 error if not found
    """
    fetched_obj = storage.get("State", str(state_id))
    if fetched_obj is None:
        abort(404)
    return jsonify(fetched_obj.to_json())


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def state_put(state_id):
    """
    Updates a specific State object by ID
    :param state_id: State object ID
    :return: JSON of the updated State object or error codes 400/404
    """
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, 'Not a JSON')

    fetched_obj = storage.get("State", str(state_id))
    if fetched_obj is None:
        abort(404)

    for key, val in state_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fetched_obj, key, val)
    fetched_obj.save()
    return jsonify(fetched_obj.to_json())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def state_delete_by_id(state_id):
    """
    Deletes a State object by ID
    :param state_id: State object ID
    :return: Empty JSON dictionary with status code 200 or 404 if not found
    """
    fetched_obj = storage.get("State", str(state_id))
    if fetched_obj is None:
        abort(404)

    storage.delete(fetched_obj)
    storage.save()
    return jsonify({})
