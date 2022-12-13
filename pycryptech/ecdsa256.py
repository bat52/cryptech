#!/usr/bin/env python3

import os
import argparse

from ecdsa256_edalize import simulate, verilate, synth_trellis
from ecdsa256_yosys import synth_yosys

def cli(argv=[]):
    parser = argparse.ArgumentParser(description='ECDSA256 Command Line Interface')
    # register format options
    
    # bare tools    
    parser.add_argument("-synth",        "--synth"        , help="Synthesize with yosys", action='store_true')  

    # edalize
    parser.add_argument("-sim",          "--simulate"     , help="Simulate with icarus verilog/edalize", action='store_true' )     
    parser.add_argument("-v",            "--verilate"     , help="Simulate with verilator/edalize", action='store_true' )
    parser.add_argument("-synth_trellis","--synth_trellis", help="Synthesize with trellis/edalize", action='store_true') 

    p = parser.parse_args(argv)
    return p

def main(argv=[]):
    p = cli(argv=argv)

    # simulation
    if p.simulate:
        simulate()
    if p.verilate:
        verilate()
    
    # synthesis
    if p.synth:
        synth_yosys()
    if p.synth_trellis:
        synth_trellis()
    
    pass

if __name__ == '__main__':    
    import sys
    main(sys.argv[1:])
    pass