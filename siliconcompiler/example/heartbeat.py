#!/usr/bin/env python3

import sys
import argparse
import siliconcompiler                            # import python package

def sc_cli(argv=[]):
    parser = argparse.ArgumentParser(description='Heartbeat SiliconCompiler flow Command Line Interface')
    
    # simulation options
    parser.add_argument("-r",          "--remote_en"      , help="Run flow on remote server.", action='store_true' )

    p = parser.parse_args(argv)
    return p  

def main(remote_en = False):
    chip = siliconcompiler.Chip('heartbeat')      # create chip object
    chip.set('input', 'verilog', 'heartbeat.v')   # define list of source files
    chip.set('input', 'sdc', 'heartbeat.sdc')     # set constraints file
    chip.load_target('freepdk45_demo')            # load predefined target
    chip.set('option', 'remote', remote_en)
    chip.run()                                    # run compilation
    chip.summary()                                # print results summary
    chip.show()                                   # show layout file

if __name__ == '__main__':
    p = sc_cli(sys.argv[1:])
    main(p.remote_en)