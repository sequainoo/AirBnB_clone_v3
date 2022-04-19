#!/usr/bin/python3
"""View for user objects with default restful api actions."""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from werkzeug.exceptions import BadRequest

from models.user import User


@app_views.route('/users', strict_slashes=False)
def get_users():
    """Returns the list of all user objects"""
    users = storage.all('User')
    users = [user.to_dict()
             for user in users.values()]
    return jsonify(users)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """Returns the list of all user objects"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Not a JSON'}), 400
        if 'email' not in data:
            return jsonify({'error': 'Missing email'}), 400
        if 'password' not in data:
            return jsonify({'error': 'Missing password'}), 400
        user = User(email=data['email'],
                    password=data['password'],
                    first_name=data.get('first_name', ''),
                    last_name=data.get('last_name', ''))
        user.save()
        return jsonify(user.to_dict()), 201
    except BadRequest:
        return jsonify({'error': 'Not a JSON'}), 400


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user(user_id):
    """Returns A user by id"""
    user = storage.get('User', user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes the user object of user_id from storage"""
    # first get objec and delete from storage
    user = storage.get('User', user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Update a user with id with request json data"""
    user = storage.get('User', user_id)
    if not user:
        abort(404)
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Not a json data'}), 400
        user.password = data.get('password', user.password)
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)

        user.save()
        return jsonify(user.to_dict()), 200
    except BadRequest:
        return jsonify({'error': 'Not a json data'}), 400
