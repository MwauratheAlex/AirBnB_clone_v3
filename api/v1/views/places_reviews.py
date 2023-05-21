#!/usr/bin/python3
"""view for Place objects that handles all default RESTFul API actions"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=["GET"])
def place_reviews(place_id):
    """Retrieves the list of all Reiew objects for a given Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    place_reviews = [review.to_dict()
                     for review in storage.all(Review).values()
                     if review.place_id == place_id]
    return jsonify(place_reviews)


@app_views.route("/reviews/<review_id>", methods=["GET"])
def review(review_id):
    """Retrieves a Review object"""
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"])
def delete_review(review_id):
    """Deletes a Review object"""
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"])
def post_review(place_id):
    """Creates a Review for a Place"""
    place = storage.get(Place, place_id)
    if place is None:
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

    if data.get("text") is None:
        abort(400, "Missing text")

    review = Review(**data)
    review.place_id = place_id
    review.user_id = user_id
    review.save()

    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"])
def put_review(review_id):
    """Updates a Review object"""
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    for key, val in data.items():
        if key not in [
                "id", "user_id", "place_id", "created_at", "updated_at"]:
            setattr(review, key, val)

    review.save()
    return jsonify(review.to_dict()), 200
