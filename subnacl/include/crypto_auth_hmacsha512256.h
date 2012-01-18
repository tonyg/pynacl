int crypto_auth_hmacsha512256(unsigned char *out,const unsigned char *in,unsigned long long inlen,const unsigned char *k);
int crypto_auth_hmacsha512256_verify(const unsigned char *h,const unsigned char *in,unsigned long long inlen,const unsigned char *k);

#define crypto_auth_hmacsha512256_BYTES 32
#define crypto_auth_hmacsha512256_KEYBYTES 32
