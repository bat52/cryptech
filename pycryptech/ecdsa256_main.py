#!/usr/bin/env python3

""" cryptech ecdsa256 commands """

import argparse
import time

'''
import sys
import os
sys.path.append( os.path.abspath(os.path.join(os.path.dirname(__file__), '..') ))
'''

from ecdsa256.edalize import simulate, verilate, synth_trellis, synth_yosys_edalize
from ecdsa256.yosys import synth_yosys
from ecdsa256.pyverilator import pyverilate
from ecdsa256.myhdl import myhdl_main
from ecdsa256.siliconcompiler_wrapper import sc_main

def cli(argv=[]):
    """ cryptech ecdsa 256 main parser """
    parser = argparse.ArgumentParser(description='ECDSA256 Command Line Interface')
    # register format options

    # edalize
    parser.add_argument("-sim",          "--simulate"     , help="Simulate ", type=str, 
                        choices=['iverilog','icarus', 'pyverilator', 'verilator','myhdl',''], default ='')

    # simulation options
    parser.add_argument("-den",          "--dump_en"      , help="Dump waveforms in simulation.", action='store_true' )

    # bare tools
    parser.add_argument("-synth",        "--synth"        , help="Synthesize", type=str,
                        choices=['yosys','yosys_edalize','trellis','sc',''], default ='')

    p = parser.parse_args(argv)
    return p

def main(argv=[]):
    p = cli(argv=argv)

    start_time = time.time()

    # simulation
    if p.simulate in ['icarus','iverilog']:
        simulate(dump_en=p.dump_en)
    elif p.simulate=='verilator':
        verilate(dump_en=p.dump_en)
    elif p.simulate=='pyverilator':
        pyverilate(dump_en=p.dump_en)
    elif p.simulate=='myhdl':
        myhdl_main(dump_en=p.dump_en)
    
    # synthesis
    if p.synth=='yosys':
        synth_yosys()
    elif p.synth=='yosys_edalize':
        synth_yosys_edalize()
    elif p.synth=='trellis':
        synth_trellis()
    elif p.synth=='sc':
        sc_main(remote_en=True)
    
    end_time = time.time()

    elapsed_time = end_time - start_time
    print('Execution time:', elapsed_time, '[s]')

    pass

if __name__ == '__main__':    
    import sys
    main(sys.argv[1:])
    pass