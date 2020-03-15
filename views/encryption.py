"""
Date: Mar 14th, 2020
Dev: franco@sustemaggency.com

views/encription.py
"""

import json
import datetime
from time import gmtime, strftime


from base64 import b64encode 
from base64 import b64decode
from Crypto.Cipher import AES 
from Crypto.Random import get_random_bytes 
from flask_cors import CORS, cross_origin
from flask import session, request, jsonify, make_response
from flask import Blueprint, render_template, redirect, url_for

encryption = Blueprint('encryption', __name__)

# Grant access on CORS
CORS(encryption)


@encryption.route('/app_encryption', methods=['GET'])
def app_encryption():
    return render_template('encryption/encryption.html'), 200


@encryption.route('/encryption', methods=['POST'])
def encrypt():

    header = b"header" 
    # if request.form['data']:
    #     header = request.form['header']
    #     header = str.encode(header)
    data = request.form['data']
    data = str.encode(data)
    
    print('Data pass: {}'.format(data))
    print('Header: {}'.format(header))

    key = get_random_bytes(16) 
    cipher = AES.new(key, AES.MODE_EAX) 
    cipher.update(header) 
    ciphertext, tag = cipher.encrypt_and_digest(data) 

    json_k = [ 'nonce', 'header', 'ciphertext', 'tag' ] 
    json_v = [ b64encode(x).decode('utf-8') for x in (cipher.nonce, header, ciphertext, tag) ]
    result = dict(zip(json_k, json_v))
    session['encrypt_key'] = key
    
    return jsonify({'result': result}), 200
    

@encryption.route('/app_decryption', methods=['GET'])
def decrypt():
    return render_template('encryption/decryption.html'), 200


@encryption.route('/decryption', methods=['POST'])
def app_decryption():
    # We assume that the key was securely shared beforehand 

    key = session['encrypt_key']
    print('key: ', key)
    print('\n')

    result = {
        'nonce': request.form['nonce'],
        'header': request.form['header'],
        'ciphertext': request.form['ciphertext'],
        'tag': request.form['tag'],
    }
    print('result', result)
    print('\n')
    
    try: 
        result = str(result)
        result = result.replace('\'', '"')
        print('result: ', result)

        b64 = json.loads( result )
        json_k = [ 'nonce', 'header', 'ciphertext', 'tag' ] 
        jv = { k:b64decode(b64[k]) for k in json_k }

        cipher = AES.new(key, AES.MODE_EAX, nonce=jv['nonce']) 
        cipher.update(jv['header']) 
        plaintext = cipher.decrypt_and_verify(jv['ciphertext'], jv['tag']) 
        print("The message was: " + plaintext.decode()) 
        output = plaintext.decode()

    except (ValueError, KeyError) as err: 
        output = 'Incorrect decryption'
        print('Error: {}'.format(err))

    return jsonify({
        'message': 'Decrypt Data', 
        'result': output
    }), 200
    