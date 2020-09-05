from flask import Flask, request, jsonify

import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random

import re
import urllib
from urllib.parse import urlparse

app = Flask(__name__)
BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

password = "securedata"

def decrypt(enc, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]))

@app.route('/api/add_message/<uuid>', methods=['POST','GET'])
def add_message(uuid):
    content = request.stream.read()
    print("Raw data: ",content)
    content = content.decode('utf-8')
    content = urllib.parse.unquote(content)
    print("Parsed data: ",content)
    #extract= re.search(r'(?<=^data=).+(?=\'$)',content).group()
    extract = content.replace("data=","")
    decrypted = decrypt(extract, password)
    data = (bytes.decode(decrypted))
    print(data)
    return jsonify({"uuid":uuid})

app.run(host= '0.0.0.0',debug=True)