
from base64 import b64decode, b64encode
import struct
from Cryptodome.Hash import SHA1, HMAC
from time import time


def hmac_sha1(secret, data):
    return HMAC.new(secret, data, SHA1).digest()

def get_time_offset():
    try:
        resp = webapi.post('ITwoFactorService', 'QueryTime', 1, params={'http_timeout': 10})
    except:
        return None

    ts = int(time())
    return int(resp.get('response', {}).get('server_time', ts)) - ts    
def generate_twofactor_code(shared_secret):
    return generate_twofactor_code_for_time(b64decode(shared_secret), int(time()) + (get_time_offset() or 0))
    
def generate_twofactor_code_for_time(shared_secret, timestamp):
    hmac = hmac_sha1(bytes(shared_secret),
                     struct.pack('>Q', int(timestamp)//30)) 

    start = ord(hmac[19:20]) & 0xF
    codeint = struct.unpack('>I', hmac[start:start+4])[0] & 0x7fffffff

    charset = '23456789BCDFGHJKMNPQRTVWXY'
    code = ''

    for _ in range(5):
        codeint, i = divmod(codeint, len(charset))
        code += charset[i]
    print(code)
    return code