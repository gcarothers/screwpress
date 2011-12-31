from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

import base64


def encrypt(key, plain_text):
    plain_text = plain_text.encode('utf-8')
    pad = AES.block_size - len(plain_text) % AES.block_size 
    data = plain_text + pad * chr(pad)
    iv_bytes = get_random_bytes(AES.block_size)
    key_bytes = key
    encrypted_bytes = iv_bytes + AES.new(key_bytes, AES.MODE_CBC, iv_bytes).encrypt(data)
    encrypted_string = base64.urlsafe_b64encode(encrypted_bytes)
    return encrypted_string

def decrypt(key, encrypted_string):
    encrypted_bytes = base64.urlsafe_b64decode(encrypted_string)
    iv_bytes = encrypted_bytes[:AES.block_size]
    encrypted_bytes = encrypted_bytes[AES.block_size:]
    plain_text = AES.new(key, AES.MODE_CBC, iv_bytes).decrypt(encrypted_bytes)
    pad = ord(plain_text[-1])
    plain_text = plain_text[:-pad]
    return plain_text.decode('utf-8')
