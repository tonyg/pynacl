#!/usr/bin/env python
"""
Build and install the NaCl wrapper.
"""

import os
from distutils.core import setup, Extension

sources = []
for d in os.listdir("subnacl"):
    for fn in os.listdir(os.path.join("subnacl", d)):
        if fn.endswith(".c"):
            sources.append(os.path.join("subnacl", d, fn))

sources.append("nacl.i")

nacl_module = Extension('_nacl', sources, include_dirs=["subnacl/include"],
                        extra_compile_args=["-O2", "-funroll-loops", "-fomit-frame-pointer"])

setup (name = 'nacl',
       version = '0.1',
       author      = "Sean Lynch",
       description = """Python wrapper for NaCl""",
       ext_modules = [nacl_module],
       py_modules  = ["nacl"])
