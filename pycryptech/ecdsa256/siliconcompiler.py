#!/usr/bin/env python3

import os
import sys
import argparse
import siliconcompiler as sc                      
from ecdsa256.common import *
from pueda.common import get_source_files_alldir

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

def sc_main(src_dir = SRC_DIR_LIST, 
            inc_dir = INC_DIR_LIST,  
            constraints = CONSTRAINTS,
            remote_en = False, 
            width = 1500, height=1500, target='freepdk45_demo'):
    #sc_setenv()

    chip = sc.Chip(TOPLEVEL)                      # create chip object

    files =  get_source_files_alldir(src_dir,fmts=['.v','.sv'])
    files += get_source_files_alldir(inc_dir,fmts=['.vh','.svh'])
    chip.set('input', 'verilog', files)  # define list of source files

    chip.set('option','idir', inc_dir)

    chip.set('input', 'sdc', constraints)         # set constraints file
    chip.load_target(target)            # load predefined target
    chip.set('option', 'remote', remote_en)

    chip.set('asic', 'diearea', [(0,0), (width,height)])
    chip.set('asic', 'corearea', [(10,10), (width-10,height-10)])

    chip.set('datasheet', chip.top(), 'pin', 'vdd', 'type', 'global', 'power')
    chip.set('datasheet', chip.top(), 'pin', 'vss', 'type', 'global', 'ground')

    # chip.add('option', 'steplist', 'import')
    # chip.add('option', 'steplist', 'convert')
    # chip.add('option', 'steplist', 'syn')

    ## execute 
    chip.run() 

    ## results         
    chip.summary()                                # print results summary
    chip.show()                                   # show layout file

if __name__ == '__main__':
    p = sc_cli(sys.argv[1:])
    sc_main(p.remote_en)