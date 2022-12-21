#!/usr/bin/env python3

import os
import sys
import argparse
import siliconcompiler as sc                      
from ecdsa256_common import *
from eda_common import get_source_files_alldir

def sc_path():
    return os.path.abspath('../siliconcompiler/siliconcompiler')

def sc_pdks_path():
    scpath = sc_path()
    return os.path.join(scpath,'targets')

def sc_get_pdks():
    pdkdir = sc_pdks_path()
    flist = os.listdir(pdkdir)
    print(flist)

def sc_setenv():
    os.environ['SCPATH'] = sc_path()

def sc_cli(argv=[]):
    parser = argparse.ArgumentParser(description='ECDSA256 SiliconCompiler flow Command Line Interface')
    
    # simulation options
    parser.add_argument("-r",          "--remote_en"      , help="Run flow on remote server.", action='store_true' )

    p = parser.parse_args(argv)
    return p    

def sc_main(remote_en = False):
    #sc_setenv()

    chip = sc.Chip(TOPLEVEL)                      # create chip object
    chip.set('input', 'verilog', get_source_files_alldir(SRC_DIR_LIST + INC_DIR_LIST))  # define list of source files
    chip.set('input', 'sdc', CONSTRAINTS)         # set constraints file
    chip.load_target('freepdk45_demo')            # load predefined target
    chip.set('option', 'remote', remote_en)
    chip.run()                                    # run compilation
    # chip.summary()                                # print results summary
    # chip.show()                                   # show layout file

if __name__ == '__main__':
    p = sc_cli(sys.argv[1:])
    sc_main(p.remote_en)