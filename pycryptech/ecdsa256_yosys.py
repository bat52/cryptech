#!/usr/bin/env python3

import os
from ecdsa256_common import *
from pyeda.yosys import yosys

def synth_yosys() -> None:
    yosys( top=TOPLEVEL,
           src_dirs=SRC_DIR_LIST,
           inc_dirs=INC_DIR_LIST)    
    pass

if __name__ == '__main__':
    synth_yosys()