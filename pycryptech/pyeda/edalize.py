#!/usr/bin/env python3

import os
from edalize import *
from pyeda.common import get_source_files_alldir, vcd_view, get_inc_list, get_clean_work

def eda_get_files(dirlist,work_root,fmts=['.v','.sv','.vh'],print_en=False) -> list:
    fnames = get_source_files_alldir(dirlist,fmts=fmts)
    # print(fnames)
    
    # build list of dict as needed by edalize
    files = []
    for fname in fnames:

        if print_en:
            print(fname)

        fext = os.path.splitext(fname)[1]

        # source files
        if fext in ['.v','.vh']:
            f = {'name' : os.path.relpath(fname, work_root),
            'file_type' : 'verilogSource'}
        elif fext in ['.sv','.svh']:
            f = {'name' : os.path.relpath(fname, work_root),
            'file_type' : 'systemVerilogSource'}
        elif fext in ['.c','.cpp','.h']:
            f = {'name' : os.path.relpath(fname, work_root),
            'file_type' : 'cSource'}
        else:
            print('unknown file extension for file %s !!!' % fname)
            f = {'name' : os.path.relpath(fname, work_root),
            'file_type' : 'unknown'}
                    
        files.append(f)     

    return files

def icarus(simname='', top='', src_dirs = [], inc_dirs = [], dump_en = True) -> None:
    # tool
    tool = 'icarus'
    work_root = get_clean_work(tool,True)

    iverilog_options = []
    if dump_en:
        iverilog_options = iverilog_options + [
            '-DDUMP_EN', 
            '-DDUMP_LEVEL=0', 
            '-DDUMP_MODULE=%s' % top
            ]

    # get design files
    files = eda_get_files(src_dirs, work_root, fmts=['.v'])

    # get include directories
    options = iverilog_options + get_inc_list(inc_dirs,work_root)
    tool_options = {
        tool :
            {
            'iverilog_options'  : options,
        }
    }

    edam = {
    'files'        : files,
    'name'         : simname,
    'toplevel'     : top,
    'tool_options' : tool_options
    }

    backend = get_edatool(tool)(edam=edam,
                                work_root=work_root)

    # os.makedirs(work_root)
    backend.configure()
    backend.build()
    backend.run()

    if dump_en:
        dump_file = 'dump.vcd'
        vcd_view(os.path.join(work_root, dump_file))

def verilator(simname='', top='', src_dir=[], inc_dir = [], 
              options = [],
              dump_en = True, dump_fst = False, gtkw='') -> None:
    # tool
    tool = 'verilator'
    work_root = get_clean_work(tool)

    verilator_options = ['--top-module %s' % top ] + options

    if dump_en:
        verilator_options += ['--trace']
        if dump_fst:
            verilator_options += ['--trace-fst', '-CFLAGS -DDUMP_FST']

    # get design files
    files = eda_get_files(src_dir, work_root, fmts=['.v','.vh','.cpp','.c'])

    # get include directories
    options = verilator_options + get_inc_list(inc_dir,work_root)
    tool_options = {
        tool :
            {
            'verilator_options'  : options,
        }
    }

    edam = {
    'files'        : files,
    'name'         : simname,
    'toplevel'     : top,
    'tool_options' : tool_options
    }

    backend = get_edatool(tool)(edam=edam,
                                work_root=work_root)

    os.makedirs(work_root)
    backend.configure()
    backend.build()
    backend.run()

    if dump_en:
        if dump_fst:
            dump_file = 'dump.fst'
        else:
            dump_file = 'dump.vcd'
        vcd_view( os.path.join(work_root, dump_file), 
                  gtkw, '-o')

def trellis(simname='',top='',src_dir=[], inc_dir=[]) -> None:

    # tool
    tool = 'trellis'
    work_root = get_clean_work(tool)
    
    # get design files
    files = eda_get_files(src_dir, work_root, fmts=['.v','.vh'])

    # get include directories
    options = get_inc_list(inc_dir,prefix='read -incdir ')

    tool_options = {
        tool :
            {
            'trellis_options'  : {'yosys_synth_options' : options},
        }
    }

    edam = {
    'files'        : files,
    'name'         : simname,
    'toplevel'     : top,
    'tool_options' : tool_options
    }

    backend = get_edatool(tool)(edam=edam,
                                work_root=work_root)

    os.makedirs(work_root)
    backend.configure()
    backend.build()
    backend.run()

def yosys(simname='',top='',src_dir=[], inc_dir=[]) -> None:

    # tool
    tool = 'yosys'
    work_root = get_clean_work(tool)
    
    # get design files
    files = eda_get_files(src_dir, work_root, fmts=['.v','.vh'])
    # files = eda_get_files(SRC_DIR_LIST, work_root, fmts=['.v'])

    # get include directories
    # files += get_inc_list(inc_dir)
    # files += INC_DIR_LIST

    tool_options = {
        tool :
            {
            # 'incdirs' : INC_DIR_LIST,
            # 'yosys_synth_options'  : options,
            'arch': 'ice40',
        },
        
    }

    edam = {
    'files'        : files,
    'name'         : simname,
    'toplevel'     : top,
    'tool_options' : tool_options
    }

    backend = get_edatool(tool)(edam=edam,
                                work_root=work_root)

    os.makedirs(work_root)
    backend.configure()
    backend.build()
    backend.run()