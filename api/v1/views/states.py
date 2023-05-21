#!/usr/bin/python3
"""view for State objects that handles all default RESTFul API actions"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"])
def states():
    """Retrieves the list of all State objects"""
    states = [state.to_dict() for state in storage.all(State).values()]

    return jsonify(states)


@app_views.route("/states/<state_id>", methods=["GET"])
def state(state_id):
    """Retrieves a State object"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("states/<state_id>", methods=["DELETE"])
def delete(state_id):
    """Deletes a State object:: DELETE /api/v1/states/<state_id>"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"])
def post_state():
    """Creates a State: POST /api/v1/states"""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if data.get("name") is None:
        abort(400, "Missing name")

    state = State(**data)
    state.save()

    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"])
def put_state(state_id):
    """Updates a State object: PUT /api/v1/states/<state_id>"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    for key, val in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, val)

    state.save()
    return jsonify(state.to_dict()), 200
