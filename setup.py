#!/usr/bin/env python
"""
Build and install the NaCl wrapper.

Environment variables:
NACL_DIR     - location of NaCl's main directory. The INCLUDE and LIB
               build directories are found automatically

THESE ENVIRONMENT VARIABLES ARE NOW OPTIONAL
NACL_INCLUDE - location of NaCl's include files. Not needed if they're
               in a normal system location.
NACL_LIB     - location of libnacl.(a|dll) and randombytes.o. Probably
               needed no matter what because of how we find randombytes.o.

"""

import sys, os, platform, re
from distutils.core import setup, Extension

arch = platform.uname()[4]
hostname = platform.node()
shost = re.sub(r'[^a-zA-Z0-9]+', '', hostname.split(".")[0])

# http://docs.python.org/library/platform.html#platform.architecture
# recommends this to test the 64-bitness of the current interpreter:
#  is_64bits = sys.maxsize > 2**32

if arch == 'x86_64':
    arch='amd64'
if arch in ['i686','oi586','i486','i386']:
    arch='x86'

EMBEDDED_NACL = "nacl-20110221"
implementations = [
    ("crypto_auth", "hmacsha256", "ref"),
    ("crypto_auth", "hmacsha512256", "ref"),
    ("crypto_box", "curve25519xsalsa20poly1305", "ref"),
    ("crypto_core", "hsalsa20", "ref"), # or ref2
    ("crypto_core", "salsa20", "ref"),
    ("crypto_core", "salsa2012", "ref"),
    ("crypto_core", "salsa208", "ref"),
    ("crypto_hash", "sha256", "ref"),
    ("crypto_hash", "sha512", "ref"),
    ("crypto_hashblocks", "sha256", "ref"), # or inplace
    ("crypto_hashblocks", "sha512", "ref"), # or inplace
    ("crypto_onetimeauth", "poly1305", "ref"), # or 53, amd64, x86
    ("crypto_scalarmult", "curve25519", "ref"), # or athlon, donna_c64
    ("crypto_secretbox", "xsalsa20poly1305", "ref"),
    ("crypto_sign", "edwards25519sha512batch", "ref"),
    ("crypto_stream", "aes128ctr", "portable"), # or core2
    ("crypto_stream", "salsa20", "ref"), # or x86_xmm5, amd64_xmm6
    ("crypto_stream", "salsa2012", "ref"), # or x86_xmm5, amd64_xmm6
    ("crypto_stream", "salsa208", "ref"), # or x86_xmm5, amd64_xmm6
    ("crypto_stream", "xsalsa20", "ref"),
    ("crypto_verify", "16", "ref"),
    ("crypto_verify", "32", "ref"),
]

sources = []
def add_sources_from(d):
    for fn in os.listdir(d):
        if fn[-2] == "." and fn[-1] in "csS":
            sources.append(os.path.join(d, fn))
for op, algo, impl in implementations:
    d = os.path.join(EMBEDDED_NACL, op, algo, impl)
    add_sources_from(d)
sources.append(os.path.join(EMBEDDED_NACL, "randombytes", "devurandom.c"))
for s in sources:
    print s

#include_dirs = [os.path.join(BUILD_DIR, "include", arch)]
include_dirs = []

nacl_module = Extension('_nacl', sources,
                        include_dirs=include_dirs,
                        extra_compiler_args=['-fPIC'],
                        extra_link_args=['-fPIC'])

setup (name = 'nacl',
       version = '0.1',
       author      = "Sean Lynch",
       description = """Python wrapper for NaCl""",
       ext_modules = [nacl_module],
       py_modules  = ["nacl"])
