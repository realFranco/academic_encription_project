"""
Date: March 14, 2020
Dev: f97gp1@gmail.com

Ref: 
> https://pycryptodome.readthedocs.io/en/latest/src/cipher/modern.html
> https://en.wikipedia.org/wiki/Authenticated_encryption
> https://en.wikipedia.org/wiki/EAX_mode

Requirement:
sudo python3 -m pip install pycryptodome


"""

import json 
from base64 import b64encode 
from Crypto.Cipher import AES 
from Crypto.Random import get_random_bytes 

header = b"header" 
data = b"secret" 
key = get_random_bytes(16) 
cipher = AES.new(key, AES.MODE_EAX) 
cipher.update(header) 
ciphertext, tag = cipher.encrypt_and_digest(data) 

json_k = [ 'nonce', 'header', 'ciphertext', 'tag' ] 
json_v = [ b64encode(x).decode('utf-8') for x in (cipher.nonce, header, ciphertext, tag) ] 
result = json.dumps(dict(zip(json_k, json_v))) 

o_key = str(key)

print(result)       
print(o_key)


# import json 
from base64 import b64decode 
# from Crypto.Cipher import AES 

# We assume that the key was securely shared beforehand 
try: 
    o_key = str(key)
    print(o_key)

    o_key = o_key.encode()
    o_key = str(o_key)[2:-1].replace('\\\\', '\\') 

    o_key = bytes(o_key)
    
    print(o_key)
    print(type(key), type(o_key))
    print(key == o_key)

    b64 = json.loads(result) 
    json_k = [ 'nonce', 'header', 'ciphertext', 'tag' ] 
    jv = {k:b64decode(b64[k]) for k in json_k} 

    cipher = AES.new(key, AES.MODE_EAX, nonce=jv['nonce']) 
    cipher.update(jv['header']) 
    plaintext = cipher.decrypt_and_verify(jv['ciphertext'], jv['tag']) 
    print("The message was: " + plaintext.decode())  # The message was: header
except (ValueError, KeyError): 
    print("Incorrect decryption")
