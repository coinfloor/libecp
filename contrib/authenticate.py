# -*- coding: utf-8 -*-
import base64
import hashlib
import subprocess
import os
import json



def build_authenticate_message(user_id, auth_cookie, passphrase, server_nonce):
    """Build authentication message

    Coinfloor provides the following authentication details for their api:
    https://github.com/coinfloor/API/blob/master/AUTH.md
    This function uses their `sign_secp224k1` utility, provided in this repository.


    Args:
        user_id (int): numeric user ID
        auth_cookie (str): authentication cookie (in base64)
        passphrase (str): passphrase (in UTF-8)
        server_nonce (str): server nonce (in base64)

    Returns:
        string: The json string that can be sent to the server for authentication

    """

    # Convert the arugments to  bytestrings
    user_id_hex = '%016.0x' % user_id # 16 nibbles = 64 bits
    user_id_bytes = user_id_hex.decode('hex')
    servernonce_bytes = base64.b64decode(server_nonce)
    passphrase_bytes = passphrase.decode('utf-8')


    # Get random bytes from the system's non-blocking random device, urandom
    clientnonce_bytes = os.urandom(16)
    clientnonce_base64 = base64.b64encode(clientnonce_bytes)

    message_40_bytes = user_id_bytes + servernonce_bytes + clientnonce_bytes
    private_key_bytes = user_id_bytes + passphrase_bytes

    private_key_sha224hash = hashlib.sha224(private_key_bytes).digest()
    message_sha224hash = hashlib.sha224(message_40_bytes).digest()

    proc = subprocess.Popen(['./sign_secp224k1'],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            )
    stdout_value = proc.communicate(private_key_sha224hash + message_sha224hash)[0]

    sig_r = stdout_value[0:28]
    sig_s = stdout_value[28:]

    sig_r_base64 = base64.b64encode(sig_r)
    sig_s_base64 = base64.b64encode(sig_s)


    returndict = {
        'method' : 'Authenticate',
        'user_id' : user_id,
        'cookie' : auth_cookie,
        'nonce' : clientnonce_base64,
        'signature' : [
            sig_r_base64,
            sig_s_base64
            ]}


    return json.dumps(returndict)


if __name__=='__main__':
    import pprint
    # Use the default values from https://github.com/coinfloor/API/blob/master/AUTH.md
    USER_ID = 1
    COOKIE = 'HGREqcILTz8blHa/jsUTVTNBJlg='
    PASSPHRASE = 'opensesame'

    SERVER_NONCE = 'azRzAi5rm1ry/l0drnz1vw=='

    pprint.pprint(build_authenticate_message(USER_ID, COOKIE, PASSPHRASE, SERVER_NONCE))
