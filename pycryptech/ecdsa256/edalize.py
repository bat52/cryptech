#!/usr/bin/env python3

import argparse
import time
from pueda.edalize import icarus, verilator, get_dump_dirs
from ecdsa256.common import *
from pyverilator.verilator_tools import verilator_verilog_tb_ok

def simulate(dump_en = True) -> None:
    icarus(
        simname=SIMNAME,
        top=TBTOPLEVEL,
        src_dirs = SRC_DIR_LIST + TB_DIR_LIST,
        inc_dirs = INC_DIR_LIST + TB_INC_LIST,
        dump_en=dump_en)

def verilate(dump_en = False, dump_fst = True) -> None:

    if verilator_verilog_tb_ok():
        print('verilator uses verilog testbench')
        # tested with verilator 5.021
        inc_dump_dir, src_dump_dir = get_dump_dirs()
        verilator(simname=SIMNAME,
                top=TBTOPLEVEL, 
                src_dir = SRC_DIR_LIST + TB_DIR_LIST + src_dump_dir,
                inc_dir = INC_DIR_LIST + TB_INC_LIST + inc_dump_dir,
                options = ['-Wno-WIDTH', # issues at assignment
                            '-Wno-CASEINCOMPLETE', # These should probably be fixed
                            '--timescale "1ns/1ns"',
                            '--timescale-override "1ns/1ns"',
                            '--binary',
                            f'-DDUMP_MODULE={TBTOPLEVEL}',
                            '--DDUMP_LEVEL=1',
                            '--DDUMP_EN',
                            '--DTRACE_DEBUG',
                            '--DDUMP_FST'],
                dump_en = dump_en, dump_fst = dump_fst,
                plot_mode='gtkwave',
                gtkw='../verilator/tb.gtkw')
    else:
        print('verilator uses c++ testbench')
        verilator(simname=SIMNAME,
                top=TOPLEVEL, 
                src_dir = SRC_DIR_LIST + TB_VERILATOR_LIST, 
                inc_dir = INC_DIR_LIST + TB_INC_LIST, 
                options = ['-Wno-WIDTH', # issues at assignment
                            '-Wno-CASEINCOMPLETE', # These should probably be fixed
                            '--timescale "1ns/1ns"',
                            '--timescale-override "1ns/1ns"'],
                dump_en = dump_en, dump_fst = dump_fst, 
                plot_mode='gtkwave',
                gtkw='../verilator/tb.gtkw')

def synth_trellis() -> None:

    trellis(simname=SIMNAME,
            top=TOPLEVEL,
            src_dir = SRC_DIR_LIST,
            inc_dir = INC_DIR_LIST)

def synth_yosys_edalize() -> None:

    yosys_edalize(simname=SIMNAME,
          top=TOPLEVEL,
          src_dir=SRC_DIR_LIST,
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