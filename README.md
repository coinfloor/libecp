## Licence
```
Copyright 2014-2015 Coinfloor LTD.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

## Prerequisites

```
$ sudo apt-get install build-essential libgmp3-dev
```

## libecp

### Build

```
$ make libecp.so
```

## sign_secp224k1

This standalone executable utility may be called from scripts to sign Coinfloor authentication messages.
It reads from its standard input 28 bytes comprising the private key, followed by 28 bytes comprising the message hash to sign.
It then computes an elliptic-curve signature over the **secp224k1** curve and writes to its standard output 28 bytes comprising the *r* component of the signature, followed by 28 bytes comprising the *s* component.
All of these 28-byte integers are encoded with the most significant byte first.
See the `contrib` subdirectory for example scripts that make use of this utility to sign Coinfloor authentication messages.
See [AUTH.md](https://github.com/coinfloor/API/blob/master/AUTH.md) for more details about authenticating to Coinfloor.

### Build

```
$ make sign_secp224k1
```
