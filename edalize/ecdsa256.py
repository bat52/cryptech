#!/usr/bin/python3

from edalize import *
import os
import shutil

import argparse

SRC_DIR_LIST = [
    '../cryptech/cryptech_lib/memory',
    '../cryptech/cryptech_lib/multiword',
    '../cryptech/cryptech_lib/lowlevel/generic',
    '../cryptech/cryptech_lib/modular',
    '../cryptech/cryptech_ecdsalib/rtl',
    '../cryptech/cryptech_ecdsa256/rtl',
]

INC_DIR_LIST = [
    '../cryptech/cryptech_lib/lowlevel',
    '../cryptech/cryptech_ecdsalib/rtl/microcode',    
]

TB_DIR_LIST = [    
    '../cryptech/cryptech_ecdsa256/bench',
    '../icarus/src'
]

TB_INC_LIST = [    
    '../cryptech/cryptech_ecdsa256/bench',
    '../icarus/inc'
]

TB_VERILATOR_LIST = [    
    '../verilator',
]

SIMNAME    = 'ecdsa256'
TBTOPLEVEL = 'tb_curve_multiplier_256'
TOPLEVEL   = 'ecdsa256_wrapper'

def get_source_files_alldir(dirlist,fmts=['.v','.sv','.vh']) -> list:
    files = []
    # create files list
    for d in dirlist:
        files = files + get_source_files(d,fmts=fmts)

    return files

def get_source_files(directory,fmts=['.v','.sv','.vh']) -> list:
    flist = os.listdir(directory)

    foutlist = []
    for f in flist:
        # print(f)
        fbase,fext = os.path.splitext(f)
        fullfile = os.path.join(directory,f)
        if os.path.isfile(fullfile) and (fext in fmts):
            # print('file %s' % f)
            foutlist.append(fullfile)
        elif os.path.isdir(fullfile):
            # recursively browse dir
            # print('recursion %s' % f)
            ldir = os.path.join(directory,f)
            # print(ldir)
            llist = get_source_files( ldir ,fmts=fmts )
            foutlist = foutlist + llist
        pass

    # print(foutlist)

    return foutlist
    pass

def eda_get_files(dirlist,work_root,fmts=['.v','.sv','.vh'],print_en=False) -> list:
    fnames = get_source_files_alldir(dirlist,fmts=fmts)
    # print(fnames)
    
    # build list of dict as needed by edalize
    files = []
    for fname in fnames:

        if print_en:
            print(fname)

        f = {'name' : os.path.relpath(fname, work_root),
        'file_type' : 'verilogSource'}
        files.append(f)

    return files

def get_inc_list(inclist,work_root) -> list:

    outlist = []
    for ipath in inclist:
        inc = '-I' + os.path.relpath(ipath, work_root)
        outlist.append(inc)

    return outlist
    pass

def vcd_view(fname,savefname=''):
    if os.path.isfile(savefname):
        cmdstr = 'gtkwave -a %s %s' % (savefname,fname)
    else:
        cmdstr = 'gtkwave ' + fname

    # print(cmdstr)
    os.system(cmdstr)
    pass

def simulate(dump_en = True) -> None:
    # tool
    tool = 'icarus'

    work_root = os.path.join(os.getcwd() , 'work_' + tool)    
    # delete work directory
    shutil.rmtree(work_root,ignore_errors=True)

    iverilog_options = []
    if dump_en:
        dump_file = 'dump.vcd'
        iverilog_options = iverilog_options + [
            '-DDUMP_EN', 
            '-DDUMP_LEVEL=0', 
            '-DDUMP_MODULE=%s' % TBTOPLEVEL
            ]

    # get design files
    files = eda_get_files(SRC_DIR_LIST + TB_DIR_LIST, work_root, fmts=['.v'])

    # get include directories
    options = iverilog_options + get_inc_list(INC_DIR_LIST + TB_INC_LIST,work_root)
    tool_options = {
        tool :
            {
            'iverilog_options'  : options,
        }
    }

    edam = {
    'files'        : files,
    'name'         : SIMNAME,
    'toplevel'     : TBTOPLEVEL,
    'tool_options' : tool_options
    }

    backend = get_edatool(tool)(edam=edam,
                                work_root=work_root)

    # os.makedirs(work_root)
    backend.configure()
    backend.build()
    backend.run()

    if dump_en:
        vcd_view(os.path.join(work_root, dump_file))

def verilate(dump_en = True) -> None:
    # tool
    tool = 'verilator'

    work_root = os.path.join(os.getcwd() , 'work_' + tool)
    
    # delete work directory
    shutil.rmtree(work_root,ignore_errors=True)

    verilator_options = ['--top-module %s' % TOPLEVEL,
                         '-Wno-WIDTH', # issues at assignment
                         '-Wno-CASEINCOMPLETE', # These should probably be fixed
                         ] 
    if dump_en:
        verilator_options = verilator_options + [
            '--trace', 
            ]

    # get design files
    files = eda_get_files(SRC_DIR_LIST + TB_VERILATOR_LIST, work_root, fmts=['.v','.cpp','.hpp'])

    # get include directories
    options = verilator_options + get_inc_list(INC_DIR_LIST,work_root)
    tool_options = {
        tool :
            {
            'verilator_options'  : options,
        }
    }

    edam = {
    'files'        : files,
    'name'         : SIMNAME,
    'toplevel'     : TOPLEVEL,
    'tool_options' : tool_options
    }

    backend = get_edatool(tool)(edam=edam,
                                work_root=work_root)

    os.makedirs(work_root)
    backend.configure()
    backend.build()
    backend.run()

    if dump_en:
        dump_file = 'dump.vcd'
        vcd_view( os.path.join(work_root, dump_file), 
                  '../verilator/tb.gtkw')

def synth_trellis() -> None:

    # tool
    tool = 'trellis'

    work_root = os.path.join(os.getcwd() , 'work_' + tool)
    
    # delete work directory
    shutil.rmtree(work_root,ignore_errors=True)
    
    # get design files
    files = eda_get_files(SRC_DIR_LIST, work_root, fmts=['.v'])
    # files = eda_get_files(SRC_DIR_LIST+INC_DIR_LIST, work_root, fmts=['.v','.vh'])

    # get include directories
    options = get_inc_list(INC_DIR_LIST,work_root)

    tool_options = {
        tool :
            {
            'trellis_options'  : {'yosys_synth_options' : options},
        }
    }

    edam = {
    'files'        : files,
    'name'         : SIMNAME,
    'toplevel'     : TOPLEVEL,
    'tool_options' : tool_options
    }

    backend = get_edatool(tool)(edam=edam,
                                work_root=work_root)

    os.makedirs(work_root)
    backend.configure()
    backend.build()
    backend.run()

def synth_yosys() -> None:

    tool = 'yosys'
    work_root = os.path.join(os.getcwd() , 'work_' + tool)
    
    # delete work directory
    shutil.rmtree(work_root,ignore_errors=True)
    os.makedirs(work_root)

    # create yosys script
    if False:
        lines = ['read_verilog ' + s for s in get_source_files_alldir(SRC_DIR_LIST,fmts=['.v'])]
    else:
        lines = ['read_verilog ' + s for s in get_source_files_alldir(INC_DIR_LIST+SRC_DIR_LIST,fmts=['.v','.vh'])]

    lines.append('hierarchy -top %s' % TOPLEVEL)
    lines.append('write_verilog %s_full.v' % os.path.join(work_root,TOPLEVEL))

    # print output
    ysoutfile = os.path.join(work_root,'%s.ys' % TOPLEVEL)
    f = open(ysoutfile, "a")
    for l in lines: 
        # print(l)
        f.write(l + '\n')
    f.close()

    # print file
    os.system('cat %s' % ysoutfile)

    # yosys command
    # args = get_inc_list(INC_DIR_LIST,work_root)
    cmdstr = 'yosys -s %s ' % ysoutfile
    # cmdstr = cmdstr + ' '.join(args)

    print(cmdstr)

    os.system(cmdstr)

    pass

def cli(argv=[]):
    parser = argparse.ArgumentParser(description='ECDSA256 Command Line Interface')
    # register format options
    parser.add_argument("-sim",          "--simulate"     , help="Simulate with icarus verilog/edalize", action='store_true' )
    parser.add_argument("-v",            "--verilate"     , help="Simulate with verilator/edalize", action='store_true' )
    parser.add_argument("-synth_trellis","--synth_trellis", help="Synthesize with trellis/edalize", action='store_true')  
    parser.add_argument("-synth",        "--synth"        , help="Synthesize with yosys", action='store_true')  

    p = parser.parse_args(argv)
    return p

def main(argv=[]):
    p = cli(argv=argv)

    # simulation
    if p.simulate:
        simulate()
    elif p.verilate:
        verilate()
    
    # synthesis
    if p.synth:
        synth_yosys()
    elif p.synth_trellis:
        synth_trellis()
    
    pass

if __name__ == '__main__':    
    import sys
    main(sys.argv[1:])
    pass