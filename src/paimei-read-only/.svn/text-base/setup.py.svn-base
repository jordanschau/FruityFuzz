#!c:\python\python.exe

# $Id$

import os.path

from distutils.core import setup

mac = [ ]
if os.path.exists("pydbg/libmacdll.dylib"):
   mac = [ "libmacdll.dylib" ]

setup( name         = "PaiMei",
       version      = "1.2",
       description  = "PaiMei - Reverse Engineering Framework",
       author       = "Pedram Amini",
       author_email = "pedram.amini@gmail.com",
       url          = "http://www.openrce.org",
       license      = "GPL",
       packages     = ["pida", "pgraph", "pydbg", "utils"],
       package_data = {
                        "pydbg" : [ "pydasm.pyd" ] + mac,
                        "utils" : mac
                      }
)