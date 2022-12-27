#!/usr/bin/env python3

import os
import argparse
import time
from edalize import *

from ecdsa256_common import *
from eda_common import get_source_files_alldir, vcd_view, get_inc_list, get_clean_work

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

def simulate(dump_en = True) -> None:
    # tool
    tool = 'icarus'
    work_root = get_clean_work(tool,True)

    iverilog_options = []
    if dump_en:
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
        dump_file = 'dump.vcd'
        vcd_view(os.path.join(work_root, dump_file))

def verilate(dump_en = True, dump_fst = False) -> None:
    # tool
    tool = 'verilator'
    work_root = get_clean_work(tool)

    verilator_options = ['--top-module %s' % TOPLEVEL,
                         '-Wno-WIDTH', # issues at assignment
                         '-Wno-CASEINCOMPLETE', # These should probably be fixed
                         '--timescale "1ns/1ns"',
                         '--timescale-override "1ns/1ns"',
                         ] 
    if dump_en:
        verilator_options += ['--trace']
        if dump_fst:
            verilator_options += ['-DDUMP_FST']

    # get design files
    files = eda_get_files(SRC_DIR_LIST + TB_VERILATOR_LIST, work_root, fmts=['.v','.vh','.cpp','.c'])

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
        if dump_fst:
            dump_file = 'dump.fst'
        else:
            dump_file = 'dump.vcd'
        vcd_view( os.path.join(work_root, dump_file), 
                  '../verilator/tb.gtkw', '-o')

def synth_trellis() -> None:

    # tool
    tool = 'trellis'
    work_root = get_clean_work(tool)
    
    # get design files
    # files = eda_get_files(SRC_DIR_LIST, work_root, fmts=['.v'])
    files = eda_get_files(SRC_DIR_LIST+INC_DIR_LIST, work_root, fmts=['.v','.vh'])

    # get include directories
    options = get_inc_list(INC_DIR_LIST,prefix='read -incdir ')

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

def synth_yosys_edalize() -> None:

    # tool
    tool = 'yosys'
    work_root = get_clean_work(tool)
    
    # get design files
    files = eda_get_files(SRC_DIR_LIST+INC_DIR_LIST, work_root, fmts=['.v','.vh'])
    # files = eda_get_files(SRC_DIR_LIST, work_root, fmts=['.v'])

    # get include directories
    # files += get_inc_list(INC_DIR_LIST)
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

def edalize_cli(argv=[]):
    parser = argparse.ArgumentParser(description='ECDSA256 Edalize Command Line Interface')
    # register format options

    # edalize
    parser.add_argument("-sim",          "--simulate"     , help="Simulate with icarus verilog/edalize", action='store_true' )     
    parser.add_argument("-v",            "--verilate"     , help="Simulate with verilator/edalize", action='store_true' )
    parser.add_argument("-synth_trellis","--synth_trellis", help="Synthesize with trellis/edalize", action='store_true') 
    parser.add_argument("-synth_yosys"  ,"--synth_yosys"  , help="Synthesize with yosys/edalize", action='store_true') 

    # simulation options
    parser.add_argument("-den",          "--dump_en"      , help="Dump waveforms in simulation.", action='store_true' )

    p = parser.parse_args(argv)
    return p

def edalize_main(argv=[]):
    p = edalize_cli(argv=argv)

    start_time = time.time()

    # simulation
    if p.simulate:
        simulate(dump_en=p.dump_en)
    if p.verilate:
        verilate(dump_en=p.dump_en)
    
    # synthesis
    if p.synth_yosys:
        synth_yosys_edalize()
    if p.synth_trellis:
        synth_trellis()
    
    end_time = time.time()

    elapsed_time = end_time - start_time
    print('Execution time:', elapsed_time, '[s]')

    pass

if __name__ == '__main__':    
    import sys
    main(sys.argv[1:])
    pass