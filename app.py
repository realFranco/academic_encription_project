"""
Date: March 14, 2020
Dev: f97gp1@gmail.com

Encrypt Data.

Entry data to the backend.

$: python3 app.py
"""

import os
import json 

from flask import Flask
from flask_cors import CORS, cross_origin
from flask import render_template, redirect, url_for
from flask import session, request, jsonify, make_response

from views.encryption import encryption


app = Flask(__name__)
app.config['SECRET_KEY'] \
    = "f95b6589a033d93ac16e665ac4b7c112e55db60920146ac8776e36e0527743c6"

# Grant access on CORS
CORS(app)

# Registration of the endpoints sets.
app.register_blueprint(encryption)


@app.route('/', methods=['GET'])
def main_login():
    return jsonify({'message': 'Encrypt Data'}), 200


if __name__ == '__main__':
    app.run(port=8000)