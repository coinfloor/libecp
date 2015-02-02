/*
Copyright 2015 Coinfloor LTD.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

#include <stdio.h>

#include "ecp.h"

int main() {
	mp_limb_t r[MP_NLIMBS(29)], s[MP_NLIMBS(29)], d[MP_NLIMBS(29)], z[MP_NLIMBS(29)];
	uint8_t rb[28], sb[28], db[28], zb[28];
	if (fread(db, 1, sizeof db, stdin) < sizeof db || fread(zb, 1, sizeof zb, stdin) < sizeof zb) {
		return 1;
	}
#if GMP_LIMB_BITS == 32
	/*
	 * Although the field order of secp224k1 is only 28 bytes (224 bits) in
	 * length, the curve parameters are 29 bytes in length because the cyclic
	 * order of the generator point is slightly greater than 2**224.
	 *
	 * Because the input integers are 28 bytes long, we have to set the most
	 * significant word explicitly to zero on 32-bit platforms, as it will not
	 * be initialized by the bytes_to_mpn routine.
	 */
	z[sizeof *z / sizeof z - 1] = d[sizeof *d / sizeof d - 1] = 0;
#endif
	bytes_to_mpn(d, db, sizeof db);
	bytes_to_mpn(z, zb, sizeof zb);
	ecp_sign(r, s, secp224k1_p, secp224k1_a, *secp224k1_G, secp224k1_n, d, z, MP_NLIMBS(29));
	mpn_to_bytes(rb, r, sizeof rb);
	mpn_to_bytes(sb, s, sizeof sb);
	if (fwrite(rb, 1, sizeof rb, stdout) < sizeof rb || fwrite(sb, 1, sizeof sb, stdout) < sizeof sb) {
		return 2;
	}
	return 0;
}
