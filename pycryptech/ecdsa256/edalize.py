#!/usr/bin/env python3

import argparse
import time
from pueda.edalize import *
from ecdsa256.common import *

def simulate(dump_en = True) -> None:
    icarus(
        simname=SIMNAME,
        top=TBTOPLEVEL,
        src_dirs = SRC_DIR_LIST + TB_DIR_LIST,
        inc_dirs = INC_DIR_LIST + TB_INC_LIST,
        dump_en=dump_en)

def verilate(dump_en = True, dump_fst = True) -> None:

    verilator(simname=SIMNAME, 
              top=TOPLEVEL, 
              src_dir = SRC_DIR_LIST + TB_VERILATOR_LIST, 
              inc_dir = INC_DIR_LIST + TB_INC_LIST, 
              options = ['-Wno-WIDTH', # issues at assignment
                         '-Wno-CASEINCOMPLETE', # These should probably be fixed
                         '--timescale "1ns/1ns"',
                         '--timescale-override "1ns/1ns"'],
              dump_en = dump_en, dump_fst = dump_fst, 
              gtkw='../verilator/tb.gtkw')        

def synth_trellis() -> None:

    trellis(simname=SIMNAME,
            top=TOPLEVEL,
            src_dir = SRC_DIR_LIST+INC_DIR_LIST,
            inc_dir = INC_DIR_LIST)

def synth_yosys_edalize() -> None:

    yosys(simname=SIMNAME,
          top=TOPLEVEL,
          src_dir=SRC_DIR_LIST+INC_DIR_LIST,
          inc_dir=INC_DIR_LIST)

def edalize_cli(argv=[]):
    parser = argparse.ArgumentParser(description='ECDSA256 Edalize Command Line Interface')
    # register format options

    # edalize
    parser.add_argument("-sim",          "--simulate"     , help="Simulate with icarus verilog/edalize", action='store_true' )     
    parser.add_argument("-v",            "--verilate"     , help="Simulate with verilator/edalize", action='store_true' )
    parser.add_argument("-trellis",      "--synth_trellis", help="Synthesize with trellis/edalize", action='store_true') 
    parser.add_argument("-yosys"  ,      "--synth_yosys"  , help="Synthesize with yosys/edalize", action='store_true') 

    # simulation options
    parser.add_argument("-den",          "--dump_en"      , help="Dump waveforms in simulation.", action='store_true' )

    p = parser.parse_args(argv)
    return p

def edalize_main(argv=[]):
    p = edalize_cli(argv=argv)

    start_time = time.time()

    # simulation
    if p.simulate:
        simulate(dump_en=p.dump_en)
    if p.verilate:
        verilate(dump_en=p.dump_en)
    
    # synthesis
    if p.synth_yosys:
        synth_yosys_edalize()
    if p.synth_trellis:
        synth_trellis()
    
    end_time = time.time()

    elapsed_time = end_time - start_time
    print('Execution time:', elapsed_time, '[s]')

    pass

if __name__ == '__main__':    
    import sys
    edalize_main(sys.argv[1:])
    pass