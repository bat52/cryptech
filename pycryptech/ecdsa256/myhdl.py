#!/usr/bin/env python3

import os
from pyeda.myhdl import myhdl_wrapper
from ecdsa256.common import *

def myhdl_main():
    # myhdl_cosim_dut(TOPLEVEL)
    # myhdl_cosim_tb(TOPLEVEL)
    topfile = os.path.join(SRC_DIR_LIST[-1], TOPLEVEL+'.v')    
    cosim   = myhdl_wrapper(fname=topfile, src_dirs=SRC_DIR_LIST, inc_dirs=INC_DIR_LIST,
                        simname=SIMNAME, dump_en = False)
    cosim.run()

if __name__ == '__main__':
    myhdl_main()
