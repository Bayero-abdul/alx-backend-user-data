#!/usr/bin/env python3
'''session_auth module'''

from api.v1.views import app_views
from flask import request, jsonify, abort
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    '''Returns a User instance based on the email and password provided by the
    form request.
    '''
    user_email = request.form.get('email', None)
    if not user_email:
        return jsonify({"error": "email missing"}), 400

    user_pwd = request.form.get('password', None)
    if not user_pwd:
        return jsonify({"error": "password missing"}), 400

    user_objs = User.search({'email': user_email})
    if user_objs:
        user_obj = user_objs[0]
        if not User.is_valid_password(user_obj, user_pwd):
            return jsonify({"error": "wrong password"}), 401
        from api.v1.app import auth
        session_id = auth.create_session(user_obj.id)
        resp = jsonify(user_obj.to_json())
        resp.set_cookie(
            os.getenv('SESSION_NAME', '_my_session'),
            session_id)
        return resp
    return jsonify({"error": "no user found for this email"}), 404


@app_views.route(
        '/auth_session/logout',
        methods=['DELETE'],
        strict_slashes=False)
def logout():
    '''Kills a user session
    '''
    from api.v1.app import auth
    b = auth.destroy_session(request)
    if b:
        return jsonify({}), 200
    return False, abort(404)
