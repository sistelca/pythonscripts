from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import base64
import json

def encrypt_with_public_key(a_message, public_key):
    encryptor = PKCS1_OAEP.new(public_key)
    encrypted_msg = encryptor.encrypt(a_message)
    encoded_encrypted_msg = base64.b64encode(encrypted_msg)
    return encoded_encrypted_msg

key = RSA.import_key(open('/home/luis/Documents/datasets/public.pem').read())      # add the key import with import_key() or importKey()

byte_messages = [b'vSOMv8sGqqol57VE9Cec5jHB5KeGie3E4KnG92AUGr4WuQj9wX2nRSAewBYDkHaz', b'ML5lpWZKOPXLcrShDAi5NBtk5HcPzYPH0JWKjPKb4eSyx8ubpcZrxbNqY9zVGil8']

dic_cla = dict()
dic_cla['API_KEY'] = encrypt_with_public_key(byte_messages[0], key).decode("utf-8")
dic_cla['SECRECT_KEY'] = encrypt_with_public_key(byte_messages[1], key).decode("utf-8")

with open('/var/www/html/sistelca.json', 'w') as sistelca:
	json.dump(dic_cla, sistelca)


