"""
Date: March 14, 2020
Dev: f97gp1@gmail.com

Academic Encryption Project - FaCyT

Entry point to the backend.

$: python3 app.py
"""

import os
import json 

from flask import Flask
from flask_cors import CORS
from flask import render_template

from views.encryption import encryption


app = Flask(__name__)

# Grant access on CORS
CORS(app)

# Registration of the endpoints sets.
app.register_blueprint(encryption)


@app.route('/', methods=['GET'])
def app_encryption():
    return render_template('main.html'), 200


if __name__ == '__main__':
    app.run(port=8003)
