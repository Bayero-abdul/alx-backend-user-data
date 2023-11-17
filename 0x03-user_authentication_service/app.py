#!/usr/bin/env python3
"""Flask app module
"""

from flask import Flask, jsonify, request
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def basic_app():
    """Basic app
    """
    return jsonify({"message": "Bienvenue"})

@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """Registers a user
    """
    email = request.form.get('email')
    password = request.form.get('password')

    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
