#!/usr/bin/python3
"""View for amenity objects with default restful api actions."""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from werkzeug.exceptions import BadRequest

from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False)
def get_amenities():
    """Returns the list of all amenity objects"""
    amenities = storage.all('Amenity')
    amenities = [amenity.to_dict() for amenity in amenities.values()]
    return jsonify(amenities)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Returns the list of all amenity objects"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Not a JSON'}), 400
        if 'name' not in data:
            return jsonify({'error': 'Missing name'}), 400
        amenity = Amenity(name=data['name'])
        amenity.save()
        return jsonify(amenity.to_dict()), 201
    except BadRequest:
        return jsonify({'error': 'Not a JSON'}), 400


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def get_amenity(amenity_id):
    """Returns A amenity by id"""
    amenity = storage.get('Amenity', amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes the amenity object of amenity_id from storage"""
    # first get objec and delete from storage
    amenity = storage.get('Amenity', amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Update an amenity with id with request json data"""
    amenity = storage.get('Amenity', amenity_id)
    if not amenity:
        abort(404)
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Not a json data'}), 400
        amenity.name = data.get('name', amenity.name)

        amenity.save()
        return jsonify(amenity.to_dict()), 200
    except BadRequest:
        return jsonify({'error': 'Not a json data'}), 400
