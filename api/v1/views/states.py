#!/usr/bin/python3
"""View for State objects with default restful api actions."""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from werkzeug.exceptions import BadRequest

from models.state import State


@app_views.route('/states', strict_slashes=False)
@app_views.route('/states/<state_id>', strict_slashes=False)
def get_states_or_state(state_id=None):
    """Returns the list of all state objects"""
    if not state_id:
        states = storage.all('State')
        states = [state.to_dict() for state in states.values()]
        return jsonify(states)
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Deletes the state object of state_id from storage"""
    # first get objec and delete from storage
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """creates a state instance"""
    try:
        data = request.get_json(force=True)
        if 'name' not in data:
            return jsonify({'error': 'Missing name'}), 400
        data['__class__'] = 'State'
        state = State(**data)
        state.save()
        data = state.to_dict()
        return jsonify(data), 201
    except BadRequest:
        return jsonify({'error': 'Not a JSON'}), 400


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update a state with id with request json data"""
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Not a json data'}), 400
        state.name = data.get('name', state.name)

        state.save()
        return jsonify(state.to_dict()), 200

    except BadRequest:
        return jsonify({'error': 'Not a json data'}), 400
