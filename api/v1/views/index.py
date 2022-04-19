#!/usr/bin/python3
"""handle general route
    /status:    returns "status":"OK"
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """return JSON of OK status"""
    return jsonify({'status': 'OK'})
