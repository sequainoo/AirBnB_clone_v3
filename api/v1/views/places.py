#!/usr/bin/python3
"""View for place objects with default restful api actions."""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from werkzeug.exceptions import BadRequest

from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_city_places(city_id):
    """Returns the list of all place objects"""
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    places = storage.all('Place')
    places = [place.to_dict()
              for place in places.values()
              if place.city_id == city_id]
    return jsonify(places)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Returns the list of all place objects"""
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Not a JSON'}), 400
        if 'user_id' not in data:
            return jsonify({'error': 'Missing user_id'}), 400
        if not storage.get('User', data['user_id']):
            abort(404)
        if 'name' not in data:
            return jsonify({'error': 'Missing name'}), 400
        place = Place(user_id=data['user_id'],
                      name=data['name'],
                      number_rooms=data.get('number_rooms', 0),
                      number_bathrooms=data.get('number_bathrooms', 0),
                      max_guest=data.get('max_guest', 0),
                      price_by_night=data.get('price_by_night', 0),
                      latitude=data.get('latitude', 0.0),
                      longitude=data.get('longitude', 0.0),
                      description=data.get('description', ''),
                      city_id=city_id)
        place.save()
        return jsonify(place.to_dict()), 201
    except BadRequest:
        return jsonify({'error': 'Not a JSON'}), 400


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place(place_id):
    """Returns A place by id"""
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes the place object of place_id from storage"""
    # first get objec and delete from storage
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update a place with id with request json data"""
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Not a JSON'}), 400
        place.name = data.get('name', place.name)
        place.number_bathrooms = data.get('number_bathrooms',
                                          place.first_name)
        place.description = data.get('description', place.description)
        place.max_guest = data.get('max_guest', place.max_guest)
        place.price_by_night = data.get('price_by_night', place.price_by_night)
        place.latitude = data.get('latitude', place.latitude)
        place.longitude = data.get('longitude', place.longitude)
        place.description = data.get('description', place.description)

        place.save()
        return jsonify(place.to_dict()), 200
    except BadRequest:
        return jsonify({'error': 'Not a JSON'}), 400
