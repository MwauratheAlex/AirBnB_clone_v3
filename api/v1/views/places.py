#!/usr/bin/python3
"""view for Place objects that handles all default RESTFul API actions"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<city_id>/places", methods=["GET"])
def city_places(city_id):
    """Retrieves the list of all Place objects"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places = [place.to_dict()
              for place in storage.all(Place).values()
              if place.city_id == city_id]
    return jsonify(places)


@app_views.route("/places/<place_id>", methods=["GET"])
def place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    """Deletes a Place object: DELETE /api/v1/places/<place_id>"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def post_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    user_id = data.get("user_id")
    if user_id is None:
        abort(400, "Missing user_id")

    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if data.get("name") is None:
        abort(400, "Missing name")

    place = Place(**data)
    place.city_id = city_id
    place.user_id = user_id

    place.save()

    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"])
def put_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    for key, val in data.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, val)

    place.save()
    return jsonify(place.to_dict()), 200
