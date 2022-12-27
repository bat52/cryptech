#!/usr/bin/env python3

import argparse
import time

from ecdsa256_edalize import simulate, verilate, synth_trellis, synth_yosys_edalize
from ecdsa256_yosys import synth_yosys
from ecdsa256_pyverilator import pyverilate

def cli(argv=[]):
    parser = argparse.ArgumentParser(description='ECDSA256 Command Line Interface')
    # register format options
    
    # edalize
    parser.add_argument("-sim",          "--simulate"     , help="Simulate ", type=str, 
                        choices=['iverilog', 'pyverilator', 'verilator',''], default ='')

    # simulation options
    parser.add_argument("-den",          "--dump_en"      , help="Dump waveforms in simulation.", action='store_true' )

    # bare tools    
    parser.add_argument("-synth",        "--synth"        , help="Synthesize", type=str,
                        choices=['yosys','yosys_edalize','trellis',''], default ='')
    
    p = parser.parse_args(argv)
    return p

def main(argv=[]):
    p = cli(argv=argv)

    start_time = time.time()

    # simulation
    if p.simulate=='iverilog':
        simulate(dump_en=p.dump_en)
    elif p.simulate=='verilator':
        verilate(dump_en=p.dump_en)
    elif p.simulate=='pyverilator':
        pyverilate(dump_en=p.dump_en)
    
    # synthesis
    if p.synth=='yosys':
        synth_yosys()
    elif p.synth=='yosys_edalize':
        synth_yosys_edalize()
    elif p.synth=='trellis':
        synth_trellis()
    
    end_time = time.time()

    elapsed_time = end_time - start_time
    print('Execution time:', elapsed_time, '[s]')

    pass

if __name__ == '__main__':    
    import sys
    main(sys.argv[1:])
    pass