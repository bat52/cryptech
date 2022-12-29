#!/usr/bin/env python3

import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '..') )

from pyeda.common import get_source_files_alldir, get_remote_files, get_clean_work, list2str, get_inc_list

def vpi_make(src_dirs=['./'], inc_dirs=[], args = []):
    print(src_dirs)
    src = get_source_files_alldir(src_dirs,fmts=['.c'])
    inc = get_inc_list(inc_dirs)
    print(inc)

    argstr = list2str(args)
    srcstr = list2str(src)
    incstr = list2str(inc)
    cmdstr = list2str( ['iverilog-vpi', argstr, srcstr, incstr ] )
    print(cmdstr)

    os.system(cmdstr)
    pass

class myhdl_vpi(object):

    work = './'

    def __init__(self):
        self.work = get_clean_work(tool='myhdl_vpi',makedir=True)
        self._get_myhdl_vpi()
        vpi_make(src_dirs=[self.work])

    def _get_myhdl_vpi(self):

        url="https://raw.githubusercontent.com/myhdl/myhdl/master/cosimulation/icarus"
        flist = ['myhdl.c', 'myhdl_table.c', 'Makefile']

        get_remote_files(url=url,flist=flist,dstdir=self.work)

if __name__ == '__main__':
    mv = myhdl_vpi()