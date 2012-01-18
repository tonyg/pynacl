int crypto_stream_salsa20(
        unsigned char *c,unsigned long long clen,
  const unsigned char *n,
  const unsigned char *k
);
int crypto_stream_salsa20_xor(
        unsigned char *c,
  const unsigned char *m,unsigned long long mlen,
  const unsigned char *n,
  const unsigned char *k
);
