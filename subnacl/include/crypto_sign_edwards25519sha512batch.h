int crypto_sign_edwards25519sha512batch_keypair(
    unsigned char *pk,
    unsigned char *sk
    );
int crypto_sign_edwards25519sha512batch(
    unsigned char *sm,unsigned long long *smlen,
    const unsigned char *m,unsigned long long mlen,
    const unsigned char *sk
    );
int crypto_sign_edwards25519sha512batch_open(
    unsigned char *m,unsigned long long *mlen,
    const unsigned char *sm,unsigned long long smlen,
    const unsigned char *pk
    );

#define crypto_sign_edwards25519sha512batch_SECRETKEYBYTES 64
#define crypto_sign_edwards25519sha512batch_PUBLICKEYBYTES 32
#define crypto_sign_edwards25519sha512batch_BYTES 64
