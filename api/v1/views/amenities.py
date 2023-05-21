#!/usr/bin/python3
"""view for Amenity objects that handles all default RESTFul API actions"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"])
def amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = [amenity.to_dict()
                 for amenity in storage.all(Amenity).values()]

    return jsonify(amenities)


@app_views.route("/amenities/<amenity_id>", methods=["GET"])
def amenity(amenity_id):
    """Retrieves a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    """Deletes an Amenity object:: DELETE /api/v1/amenities/<amenity_id>"""
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"])
def post_amenity():
    """Creates a Amenity: POST /api/v1/amenities"""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if data.get("name") is None:
        abort(400, "Missing name")

    amenity = Amenity(**data)
    amenity.save()

    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def put_amenity(amenity_id):
    """Updates a Amenity object: PUT /api/v1/amenities/<amenity_id>"""
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    for key, val in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, val)

    amenity.save()
    return jsonify(amenity.to_dict()), 200
