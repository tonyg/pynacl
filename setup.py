#!/usr/bin/env python
"""
Build and install the NaCl wrapper.
"""

import sys, os, platform, re
from distutils.core import setup, Extension

# http://docs.python.org/library/platform.html#platform.architecture
# recommends this to test the 64-bitness of the current interpreter:
is_64bits = sys.maxsize > 2**32
# My OS-X 10.6 laptop reports platform.uname()[4]=='i386', but
# is_64bits==True, and gcc appears to use -m64 by default. The symptoms of
# getting it wrong are errors during any compilation that tries to use
# libnacl.a:
#  ld: warning: in .../libnacl.a, file is not of required architecture
#  Undefined symbols:
#    "_crypto_hash_sha512_ref", referenced from:
#        _main in ....o
#  ld: symbol(s) not found

# note that system Python will try to compile everything for multiple arches
# at once ("universal binaries"), with "-arch i386 -arch ppc -arch x86_64",
# but each libnacl.a is for just a single arch (there are two copies, in
# lib/x86/ and lib/amd64). So you can expect some harmless "not of required
# architecture" warnings when running setup.py build, probably four:
# (libnacl.a,randombytes.o) * (ppc, i386).

if is_64bits:
    arch='amd64'
else:
    arch='x86'

EMBEDDED_NACL = "nacl-20110221"
implementations = [
    ("crypto_auth", "hmacsha512256", "ref"),
    # omit crypto_auth/hmacsha256
    ("crypto_box", "curve25519xsalsa20poly1305", "ref"),
    ("crypto_core", "hsalsa20", "ref"), # or ref2
    ("crypto_core", "salsa20", "ref"),
    #("crypto_core", "salsa2012", "ref"),
    #("crypto_core", "salsa208", "ref"),
    ("crypto_hash", "sha256", "ref"),
    ("crypto_hash", "sha512", "ref"),
    ("crypto_hashblocks", "sha256", "ref"), # or inplace
    ("crypto_hashblocks", "sha512", "ref"), # or inplace
    ("crypto_onetimeauth", "poly1305", "ref"), # or 53, amd64, x86
    ("crypto_scalarmult", "curve25519", "ref"), # or athlon, donna_c64
    ("crypto_secretbox", "xsalsa20poly1305", "ref"),
    ("crypto_sign", "edwards25519sha512batch", "ref"),
    ("crypto_stream", "salsa20", "ref"), # or x86_xmm5, amd64_xmm6
    ("crypto_stream", "xsalsa20", "ref"),
    # omit these unused primitives:
    #("crypto_stream", "aes128ctr", "portable"), # or core2
    #("crypto_stream", "salsa2012", "ref"), # or x86_xmm5, amd64_xmm6
    #("crypto_stream", "salsa208", "ref"), # or x86_xmm5, amd64_xmm6
    ("crypto_verify", "16", "ref"),
    ("crypto_verify", "32", "ref"),
]

sources = []
def add_sources_from(d):
    for fn in os.listdir(d):
        if fn[-2] == "." and fn[-1] in "csS":
            sources.append(os.path.join(d, fn))
def generate_headers():
    for op, algo, impl in implementations:
        #sfn = os.path.join(EMBEDDED_NACL, op, algo, "selected")
        #if not os.path.exists(sfn):
        #    continue
        d = os.path.join(EMBEDDED_NACL, op, algo, impl)
        add_sources_from(d)
        f = open(os.path.join("my-includes", op+".h"), "w")
        f.write("#include \"%s_%s.h\"\n" % (op, algo))
        f.write("#define %s %s_%s\n" % (op, op, algo))
        f.close()
        f = open(os.path.join("my-includes", op+"_"+algo+".h"), "w")
        for line in open(os.path.join(EMBEDDED_NACL, "PROTOTYPES.c"), "r"):
            if op+"(" in line:
                f.write(line.replace(op+"(", "%s_%s_%s(" % (op,algo,impl)))
        f.write("#define %(op)s_%(algo)s %(op)s_%(algo)s_%(impl)s\n" %
                {"op": op, "algo": algo, "impl": impl})
        f.close()
    f = open(os.path.join("my-includes", "cpuid.h"), "w")
    f.write('static const char *cpuid = "none\\n";\n')
    f.close()
generate_headers()

sources.append(os.path.join(EMBEDDED_NACL, "randombytes", "devurandom.c"))
for s in sources:
    print s

include_dirs = ["my-includes"]

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
