#!/usr/bin/python3
"""View for city objects with default restful api actions."""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from werkzeug.exceptions import BadRequest

from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_state_cities(state_id):
    """Returns the list of all city objects"""
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    cities = storage.all('City')
    cities = [city.to_dict()
              for city in cities.values()
              if city.state_id == state_id]
    return jsonify(cities)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_state_city(state_id):
    """Returns the list of all city objects"""
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Not a JSON'}), 400
        if 'name' not in data:
            return jsonify({'error': 'Missing name'}), 400
        city = City(name=data['name'], state_id=state_id)
        city.save()
        return jsonify(city.to_dict()), 201
    except BadRequest:
        return jsonify({'error': 'Not a JSON'}), 400


@app_views.route('/cities/<city_id>', strict_slashes=False)
def get_city(city_id):
    """Returns A city by id"""
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes the city object of city_id from storage"""
    # first get objec and delete from storage
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    city.delete()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Update a city with id with request json data"""
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Not a json data'}), 400
        city.name = data.get('name', city.name)

        city.save()
        return jsonify(city.to_dict()), 200
    except BadRequest:
        return jsonify({'error': 'Not a json data'}), 400
