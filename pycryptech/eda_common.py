#!/usr/bin/python3

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
        fullfile = os.path.abspath(os.path.join(directory,f))
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

def get_inc_list(inclist,work_root,prefix='-I') -> list:

    outlist = []
    for ipath in inclist:
        inc = prefix + os.path.relpath(ipath, work_root)
        outlist.append(inc)

    return outlist
    pass

def vcd_view(fname,savefname='',options=''):
    if os.path.isfile(savefname):
        cmdstr = 'gtkwave %s -a %s %s' % (options, savefname,fname)
    else:
        cmdstr = 'gtkwave %s %s' % (options,fname)

    # print(cmdstr)
    os.system(cmdstr)
    pass

def get_clean_work(tool='',makedir=False):
    work_root = os.path.join(os.getcwd() , 'work_' + tool)    
    # delete work directory
    shutil.rmtree(work_root,ignore_errors=True)
    
    if makedir:
        os.makedirs(work_root)
        
    return work_root