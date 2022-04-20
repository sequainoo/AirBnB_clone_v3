#!/usr/bin/python3
"""Flask application module"""
import os

from flask import Flask, jsonify
from flask_cors import CORS

from .views.index import *
from models import storage
from .views import app_views


app = Flask(__name__)
CORS(app, origins='0.0.0.0')
app.register_blueprint(app_views)


@app.errorhandler(404)
def errorhandler(err):
    """Error handler for 404 errors"""
    return jsonify({'error': 'Not found'}), 404


@app.teardown_appcontext
def teardown(exc):
    """Tear down"""
    storage.close()


if __name__ == '__main__':
    app.run(host=os.getenv('HBNB_API_HOST'),
            port=os.getenv('HBNB_API_PORT'),
            threaded=True)
