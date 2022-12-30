#!/usr/bin/env python3

import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '..') )

from pyeda.common import get_source_files_alldir, get_remote_files, get_clean_work, list2str, get_inc_list

def vpi_make(src_dirs=['./'], inc_dirs=[], args = []):
    # print(src_dirs)
    src = get_source_files_alldir(src_dirs,fmts=['.c','.cc','.cpp'])
    inc = get_inc_list(inc_dirs)
    # print(inc)

    argstr = list2str(args)
    srcstr = list2str(src)
    incstr = list2str(inc)
    cmdstr = list2str( ['iverilog-vpi', argstr, srcstr, incstr ] )

    print('### Making VPI...')
    print(cmdstr)
    os.system(cmdstr)
    os.system('rm *.o')
    print('### Making VPI... Done')
    pass
class custom_vpi(object):
    work = './'

    def __init__(self,tool='custom_vpi',url='',flist=[],inc_dirs=[],args=[]):
        self.work = get_clean_work(tool=tool,rm_en=False) # do not remove if exist
        self._get_custom_vpi(url=url,flist=flist)

        new_inc = [os.path.join(self.work,ii) for ii in inc_dirs]
        vpi_make(src_dirs=[self.work], inc_dirs=new_inc,args=args)
        os.system('mv *.vpi %s' % self.work)

    def _get_custom_vpi(self,url,flist):
        get_remote_files(url=url,flist=flist,dstdir=self.work)

class myhdl_vpi(custom_vpi):
    def __init__(self):
        tool='myhdl_vpi'
        url="https://raw.githubusercontent.com/myhdl/myhdl/master/cosimulation/icarus"
        flist = ['myhdl.c', 'myhdl_table.c', 'Makefile']
        custom_vpi.__init__(self,tool=tool,url=url,flist=flist)

"""
class fst_vpi(custom_vpi):
    def __init__(self):
        tool='fst_vpi'
        url="https://github.com/semify-eda/fstdumper/archive/refs/heads/main.zip"
        inc_dirs=['./fstdumper-main/src', './fstdumper-main/src/config']
        args=['-DICARUS_VERILOG','-fPIC','-O2']
        custom_vpi.__init__(self,tool=tool,url=url,inc_dirs=inc_dirs,args=args)
"""

class fst_vpi(object):

    work = './'

    def __init__(self):
        tool='fst_vpi'
        url="https://github.com/semify-eda/fstdumper/archive/refs/heads/main.zip"

        self.work = get_clean_work(tool=tool,rm_en=False) # do not remove if exist
        get_remote_files(url=url,dstdir=self.work)

        cmdstr = 'cd %s/fstdumper-main && make simulation-iverilog && mv *.vpi %s && cd ..' % (self.work, self.work)
        print(cmdstr)

        os.system(cmdstr)

if __name__ == '__main__':
    # mv = myhdl_vpi()
    fv = fst_vpi()