#!/usr/bin/env python

import sys, os, time, json
from distutils import util
from compare import abbreviate_small_time

libdir = os.path.join("build",
                      "lib.%s-%s" % (util.get_platform(), sys.version[:3]))
sys.path.insert(0, libdir)

import nacl

def timeit(f, *args):
    count = 1
    while True:
        #print "trying", count
        start = time.time()
        for i in xrange(count):
            f(*args)
        end = time.time()
        elapsed = end - start
        each = elapsed / count
        #print " took %g, each=%g" % (elapsed, each)
        if count > 3 and elapsed > 1.0:
            return each, count, elapsed
        count *= 2

data = {}
def do(name, *args):
    each, count, elapsed = timeit(getattr(nacl, name), *args)
    print "%s: %s" % (name, abbreviate_small_time(each))
    data[name] = each

do("crypto_hash_sha256", b"")
do("crypto_hash_sha512", b"")

scalar0 = b"0"*32
scalar1 = b"1"*32
do("crypto_scalarmult", scalar0, scalar1)
do("crypto_scalarmult_base", scalar0)

msg = b"m"*1000
nonce = b"n"*nacl.crypto_stream_NONCEBYTES
key = b"k"*nacl.crypto_stream_KEYBYTES
do("crypto_stream", 1000, nonce, key)
do("crypto_stream_xor", msg, nonce, key)

msg = b"m"*1000
key = b"k"*nacl.crypto_auth_KEYBYTES
do("crypto_auth", msg, key)
a = nacl.crypto_auth(msg, key)
do("crypto_auth_verify", a, msg, key)

do("crypto_onetimeauth", msg, key)
a = nacl.crypto_onetimeauth(msg, key)
do("crypto_onetimeauth_verify", a, msg, key)

msg = b"m"*1000
nonce = b"n"*nacl.crypto_stream_NONCEBYTES
key = b"k"*nacl.crypto_auth_KEYBYTES
do("crypto_secretbox", msg, nonce, key)
c = nacl.crypto_secretbox(msg, nonce, key)
do("crypto_secretbox_open", c, nonce, key)

do("crypto_box_keypair")
pk1, sk1 = nacl.crypto_box_keypair()
pk2, sk2 = nacl.crypto_box_keypair()
do("crypto_box", msg, nonce, pk1, sk2)
c = nacl.crypto_box(msg, nonce, pk1, sk2)
do("crypto_box_open", c, nonce, pk2, sk1)

do("crypto_sign_keypair_fromseed", b"seed")
pk,sk = nacl.crypto_sign_keypair()
do("crypto_sign", msg, sk)
sm = nacl.crypto_sign(msg, sk)
do("crypto_sign_open", sm, pk)

open("speed.json", "w").write(json.dumps(data))
