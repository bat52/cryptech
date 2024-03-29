#!/usr/bin/env python3

from ecdsa256.common import *
from pueda.veriloggen import sim

def vg_sim():
    sim(top=TOPLEVEL,
        src_dirs=SRC_DIR_LIST,
        inc_dirs=INC_DIR_LIST
        )
    pass

if __name__ == '__main__':
    vg_sim()