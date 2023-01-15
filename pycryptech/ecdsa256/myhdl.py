#!/usr/bin/env python3

import os
from myhdl import *
from pyeda.myhdl import myhdl_cosim_wrapper, clk_driver
from ecdsa256.common import *

@block
def tb(cosim):

    ports = cosim.dut_ports()
    dut_i = cosim.dut_instance(ports=ports)

    clk_driver_i = clk_driver(ports['clk'])

    return instances()

def myhdl_main(dump_en=False):
    topfile = os.path.join(SRC_DIR_LIST[-1], TOPLEVEL+'.v')
    cosim   = myhdl_cosim_wrapper(  topfile=topfile, topmodule=TOPLEVEL, 
                                    src_dirs=SRC_DIR_LIST, inc_dirs=INC_DIR_LIST,
                                    simname=SIMNAME, dump_en=dump_en)
        
    tb_i = tb(cosim)

    cosim.sim_cfg(tb_i)
    cosim.sim_run(200)
    cosim.sim_view()

    pass

if __name__ == '__main__':
    myhdl_main()
