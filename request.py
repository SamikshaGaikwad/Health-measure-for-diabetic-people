import requests

import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random
import time

wait_time = 5
BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

password = "securedata"
server = "http://429722ca.ngrok.io"
data = "This is a secret message"

def encrypt(raw, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    raw = pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))

while(True):
    encrypted = encrypt(data, password)
    print(encrypted)
    res = requests.post(server+'/api/add_message/1234', data={"data":encrypted})
    if res.ok:
        print (res.json())
    time.sleep(wait_time)