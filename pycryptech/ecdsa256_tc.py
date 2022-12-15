#!/usr/bin/env python3

"""  Values from "Suite B Implementer's Guide to FIPS 186-3 (ECDSA)" 
"""

class ecdsaTc(object):
    k = []
    qx = []
    qy = []

    def __init__(self, k = [], qx = [], qy = []):
        self.k = k
        self.qx = qx
        self.qy = qy
        pass

    pass

ECDSA_P256_NSA_TC1 = ecdsaTc(
    [0x70a12c2d, 0xb16845ed, 0x56ff68cf, 0xc21a472b,
	 0x3f04d7d6, 0x851bf634, 0x9f2d7d5b, 0x3452b38a], # K
    [0x8101ece4, 0x7464a6ea, 0xd70cf69a, 0x6e2bd3d8,
	 0x8691a326, 0x2d22cba4, 0xf7635eaf, 0xf26680a8],  # QX
    [0xd8a12ba6, 0x1d599235, 0xf67d9cb4, 0xd58f1783,
	 0xd3ca43e7, 0x8f0a5aba, 0xa6240799, 0x36c0c3a9]  # QY
    )

ECDSA_P256_NSA_TC2 = ecdsaTc(
    [0x580ec00d, 0x85643433, 0x4cef3f71, 0xecaed496,
	 0x5b12ae37, 0xfa47055b, 0x1965c7b1, 0x34ee45d0], # K
    [0x7214bc96, 0x47160bbd, 0x39ff2f80, 0x533f5dc6,
	 0xddd70ddf, 0x86bb8156, 0x61e805d5, 0xd4e6f27c],  # QX
    [0x8b81e3e9, 0x77597110, 0xc7cf2633, 0x435b2294,
	 0xb7264298, 0x7defd3d4, 0x007e1cfc, 0x5df84541]  # QY
    )