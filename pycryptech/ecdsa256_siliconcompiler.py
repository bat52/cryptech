#!/usr/bin/env python3

import os
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

    # export SCPATH=/home/marco/.local/lib/python3.10/site-packages/siliconcompiler/pdks

def sc_main(remote_en = True):
    #sc_setenv()

    chip = sc.Chip(TOPLEVEL)                      # create chip object
    chip.set('input', 'verilog', get_source_files_alldir(INC_DIR_LIST))   # define list of source files
    chip.add('input', 'verilog', get_source_files_alldir(SRC_DIR_LIST))   # define list of source files
    chip.set('input', 'sdc', CONSTRAINTS)         # set constraints file
    chip.load_target('freepdk45_demo')            # load predefined target
    chip.set('option', 'remote', remote_en)
    chip.run()                                    # run compilation
    chip.summary()                                # print results summary
    chip.show()                                   # show layout file

if __name__ == '__main__':
    # sc_setenv()
    # print(os.environ['SCPATH'])
    sc_main()