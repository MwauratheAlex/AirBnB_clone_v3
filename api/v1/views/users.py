#!/usr/bin/python3
"""view for User objects that handles all default RESTFul API actions"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"])
def users():
    """Retrieves the list of all User objects"""
    users = [user.to_dict() for user in storage.all(User).values()]

    return jsonify(users)


@app_views.route("/users/<user_id>", methods=["GET"])
def user(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)

    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Deletes a User object:: DELETE /api/v1/users/<user_id>"""
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"])
def post_user():
    """Creates a User: POST /api/v1/users"""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if data.get("email") is None:
        abort(400, "Missing email")
    if data.get("password") is None:
        abort(400, "Missing password")

    user = User(**data)
    user.save()

    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"])
def put_user(user_id):
    """Updates a User object: PUT /api/v1/users/<user_id>"""
    user = storage.get(User, user_id)

    if user is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    for key, val in data.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, val)

    user.save()
    return jsonify(user.to_dict()), 200
