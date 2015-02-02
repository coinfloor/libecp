<?php

function pack64_be($v) {
	return pack('NN', $v >> 32, $v);
}

function build_authenticate_message(
	$user_id, // numeric user ID
	$auth_cookie, // authentication cookie (in base64)
	$passphrase, // passphrase (in UTF-8)
	$server_nonce // server nonce (in base64)
) {
	// pseudo-randomly choose a 16-byte client nonce
	$client_nonce = openssl_random_pseudo_bytes(16);

	// private key is the SHA-224 digest of the 64-bit user ID and the UTF-8-encoded passphrase
	$private_key = hash('sha224', pack64_be($user_id) . $passphrase, TRUE);

	// message to sign is the concatenation of the 64-bit user ID, server nonce, and client nonce
	$message_to_sign = hash('sha224', pack64_be($user_id) . base64_decode($server_nonce) . $client_nonce, TRUE);

	// spawn the sign_secp224k1 utility as an external process
	$proc = proc_open('./sign_secp224k1', array(
		array('pipe', 'r'), // fd 0 is standard input to the process
		array('pipe', 'w'), // fd 1 is standard output from the process
		STDERR // fd 2 inherits the standard error stream from the PHP process
	), $pipes) or die;

	// write the private key to the utility's standard input
	fwrite($pipes[0], $private_key);

	// write the SHA-224 hash of the message to the utility's standard input
	fwrite($pipes[0], hash('sha224', $message, TRUE));

	// close PHP's end of the pipe connected to the utility's standard input
	fclose($pipes[0]);

	// read the signature from the utility's standard output
	$sig_r = fread($pipes[1], 28); // 28-byte "r" component of signature
	$sig_s = fread($pipes[1], 28); // 28-byte "s" component of signature

	// close PHP's end of the pipe connected to the utility's standard output
	fclose($pipes[1]);

	// close the handle to the external process
	proc_close($proc);

	// build and return the Authenticate message
	return array(
		'method' => 'Authenticate',
		'user_id' => intval($user_id),
		'cookie' => $auth_cookie,
		'nonce' => base64_encode($client_nonce),
		'signature' => array(
			base64_encode($sig_r),
			base64_encode($sig_s)
		)
	);
}
