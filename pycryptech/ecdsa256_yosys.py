#!/usr/bin/env python3

import os
from ecdsa256_common import *
from eda_common import get_source_files_alldir, get_clean_work

def synth_yosys() -> None:

    tool = 'yosys'
    work_root = get_clean_work(tool,True)

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