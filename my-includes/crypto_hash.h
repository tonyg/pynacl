#ifndef crypto_hash_H
#define crypto_hash_H

#ifdef crypto_hash_sha512_H
#include "crypto_hash_sha512.h"
#define crypto_hash crypto_hash_sha512
#define crypto_hash_BYTES crypto_hash_sha512_BYTES
#define crypto_hash_PRIMITIVE "sha512"
#define crypto_hash_IMPLEMENTATION crypto_hash_sha512_IMPLEMENTATION
#define crypto_hash_VERSION crypto_hash_sha512_VERSION
#endif

#ifdef crypto_hash_sha256_H
#include "crypto_hash_sha256.h"
#define crypto_hash crypto_hash_sha256
#define crypto_hash_BYTES crypto_hash_sha256_BYTES
#define crypto_hash_PRIMITIVE "sha256"
#define crypto_hash_IMPLEMENTATION crypto_hash_sha256_IMPLEMENTATION
#define crypto_hash_VERSION crypto_hash_sha256_VERSION
#endif

#endif
