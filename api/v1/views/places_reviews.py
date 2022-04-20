#!/usr/bin/python3
"""View for review objects with default restful api actions."""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from werkzeug.exceptions import BadRequest

from models.review import Review


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get_reviews(place_id):
    """Returns the list of all review objects"""
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    reviews = storage.all('Review')
    reviews = [review.to_dict()
               for review in reviews.values()
               if review.place_id == place_id]
    return jsonify(reviews)


@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Returns the list of all review objects"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Not a JSON'}), 400
        if 'user_id' not in data:
            return jsonify({'error': 'Missing user_id'}), 400
        if 'text' not in data:
            return jsonify({'error': 'Missing text'}), 400
        review = Review(user_id=data['user_id'],
                        place_id=place_id,
                        text=data['text'])
        review.save()
        return jsonify(review.to_dict()), 201
    except BadRequest:
        return jsonify({'error': 'Not a JSON'}), 400


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def get_review(review_id):
    """Returns A review by id"""
    review = storage.get('Review', review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes the review object of review_id from storage"""
    # first get objec and delete from storage
    review = storage.get('Review', review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Update an review with id with request json data"""
    review = storage.get('Review', review_id)
    if not review:
        abort(404)
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Not a JSON'}), 400
        review.text = data.get('text', review.text)

        review.save()
        return jsonify(review.to_dict()), 200
    except BadRequest:
        return jsonify({'error': 'Not a JSON'}), 400
