import os
import hashlib
from base64 import b64decode, b64encode
import subprocess

# Parameters:
# - user_id (int): numeric user ID
# - auth_cookie (str): authentication cookie (in base64)
# - passphrase (unicode): passphrase
# - server_nonce (str): server nonce (in base64)
def build_authenticate_message(user_id, auth_cookie, passphrase, server_nonce):
	# [python 3.2+] user_id_bytes = user_id.to_bytes(8, "big")
	user_id_bytes = ("%016x" % user_id).decode("hex")

	# pseudo-randomly choose a 16-byte client nonce
	client_nonce = os.urandom(16)

	# private key is the SHA-224 digest of the 64-bit user ID and the UTF-8 encoded passphrase
	private_key = hashlib.sha224(user_id_bytes + passphrase.encode("utf8")).digest()

	# message to sign is the concatenation of the 64-bit user ID, server nonce, and client nonce
	message_to_sign = user_id_bytes + b64decode(server_nonce) + client_nonce

	# spawn the sign_secp224k1 utility as an external process
	proc = subprocess.Popen(["./sign_secp224k1"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

	# write the private key and the SHA-224 hash of the message to the utility's standard input
	# and read the signature from the utility's standard output
	sig = proc.communicate(private_key + hashlib.sha224(message_to_sign).digest())[0]

	return {
		"method": "Authenticate",
		"user_id": user_id,
		"cookie": auth_cookie,
		"nonce": b64encode(client_nonce),
		"signature": [
			b64encode(sig[0:28]),
			b64encode(sig[28:])
		]
	}
