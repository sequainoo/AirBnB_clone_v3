#!/usr/bin/python3
import os

from flask import Flask, jsonify

from .views.index import *
from models import storage
from .views import app_views

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')

@app.teardown_appcontext
def teardown(exc):
    """Tear down"""
    storage.close()

if __name__ == '__main__':
    app.run(host=os.getenv('HBNB_API_HOST'),
            port=os.getenv('HBNB_API_PORT'),
            threaded=True)
