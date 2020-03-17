"""
Date: Mar 14th, 2020
Dev: f97gp1@gmail.com

views/encription.py

Ref: 
> https://pycryptodome.readthedocs.io/en/latest/src/cipher/modern.html
> https://en.wikipedia.org/wiki/Authenticated_encryption
> https://en.wikipedia.org/wiki/EAX_mode
"""


import json
import codecs

from base64 import b64encode, b64decode
from Crypto.Cipher import AES 
from Crypto.Random import get_random_bytes 
from flask_cors import CORS
from flask import Blueprint, request, session, jsonify

encryption = Blueprint('encryption', __name__)

# Grant access on CORS
CORS(encryption)


@encryption.route('/encryption', methods=['POST'])
def encrypt():
    
    header = str.encode(request.args['header'])
    data = str.encode(request.args['data'])
    
    key = get_random_bytes(16)

    cipher = AES.new(key, AES.MODE_EAX) 
    cipher.update(header) 
    ciphertext, tag = cipher.encrypt_and_digest(data) 

    json_k = [ 'nonce', 'header', 'ciphertext', 'tag' ] 
    json_v = [ b64encode(x).decode('utf-8') for x in (cipher.nonce, header, ciphertext, tag) ]
    result = dict(zip(json_k, json_v))

    # Encode the key into unidocde to pass it through flask's request.
    q_key = str(key).encode('utf-8')[2:-1]

    result['q_key'] = q_key

    return jsonify({'result': result}), 201
    

@encryption.route('/decryption', methods=['POST'])
def app_decryption():
    # We assume that the key was securely shared beforehand 
    result = request.args.to_dict()

    q_key = result.pop('q_key')

    # Decocode the key into byte to pass it through the EAX cipher.
    key = codecs.escape_decode(q_key)[0]

    try:
        # Static
        json_k = [ 'nonce', 'header', 'ciphertext', 'tag' ]

        result = str(result).replace('\'', '"')

        b64 = json.loads(result)
        b64 = { k:b64[k].replace(' ', '+') for k in json_k }
        jv = { k:b64decode(b64[k]) for k in json_k }

        cipher = AES.new(key, AES.MODE_EAX, nonce=jv['nonce']) 
        cipher.update(jv['header']) 
        plaintext = cipher.decrypt_and_verify(jv['ciphertext'], jv['tag']) 

        output = plaintext.decode()

    except (ValueError, KeyError) as err: 
        output = err

    return jsonify({
        'message': 'Decrypt Data', 
        'result': output
    }), 200
    