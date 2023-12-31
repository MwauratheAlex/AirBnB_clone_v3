#!/usr/bin/python3
"""view for City objects that handles all default RESTFul API actions"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"])
def state_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict()
              for city in storage.all(City).values()
              if city.state_id == state_id]
    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=["GET"])
def city(city_id):
    """Retrieves a City object"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def post_city(state_id):
    """Creates a City object"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if data.get("name") is None:
        abort(400, "Missing name")

    city = City(**data)
    city.state_id = state_id
    city.save()

    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"])
def put_city(city_id):
    """Updates a City object"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    for key, val in data.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, val)

    city.save()
    return jsonify(city.to_dict()), 200
