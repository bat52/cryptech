#!/usr/bin/python3

from edalize import *
import os
import shutil

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

def vcd_view(fname):
    os.system('gtkwave ' + fname)
    pass

def simulate(dump_en = True) -> None:
    simname = 'ecdsa256'
    toplevel = 'tb_curve_multiplier_256'
    work_root = os.path.join(os.getcwd() , 'work')
    
    # delete work directory
    shutil.rmtree(work_root,ignore_errors=True)

    # tool
    tool = 'icarus'
    
    src_dir_list = [
        '../cryptech/cryptech_lib/memory',
        '../cryptech/cryptech_lib/multiword',
        '../cryptech/cryptech_lib/lowlevel/generic',
        '../cryptech/cryptech_lib/modular',
        '../cryptech/cryptech_ecdsalib/rtl',
        '../cryptech/cryptech_ecdsa256/rtl',
    ]

    tb_dir_list = [    
        '../cryptech/cryptech_ecdsa256/bench',    
    ]

    inc_dir_list = [
        '../cryptech/cryptech_lib/lowlevel',
        '../cryptech/cryptech_ecdsalib/rtl/microcode',
        '../cryptech/cryptech_ecdsa256/bench',
    ]

    iverilog_options = []
    if dump_en:
        src_dir_list = src_dir_list + ['../%s/src' % tool ]
        inc_dir_list = inc_dir_list + ['../%s/inc' % tool ]
        dump_file = 'dump.vcd'
        iverilog_options = iverilog_options + [
            '-DDUMP_EN', 
            '-DDUMP_LEVEL=0', 
            '-DDUMP_MODULE=%s' % toplevel
            ]

    # get design files
    files = eda_get_files(src_dir_list+tb_dir_list, work_root, fmts=['.v'])

    # get include directories
    iverilog_options = iverilog_options + get_inc_list(inc_dir_list,work_root)
    tool_options = {
        tool :
            {
            'iverilog_options'  : iverilog_options,
        }
    }

    edam = {
    'files'        : files,
    'name'         : simname,
    'toplevel'     : toplevel,
    'tool_options' : tool_options
    }

    backend = get_edatool(tool)(edam=edam,
                                work_root=work_root)

    os.makedirs(work_root)
    backend.configure()
    backend.build()
    backend.run()

    if dump_en:
        vcd_view(os.path.join(work_root, dump_file))

if __name__ == '__main__':    
    simulate()
    pass