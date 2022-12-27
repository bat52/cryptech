#!/usr/bin/env python3

import os
from ecdsa256_common import *
from eda_common import get_source_files_alldir, get_clean_work, get_inc_list, write_file_lines

def synth_yosys() -> None:

    tool = 'yosys'
    work_root = get_clean_work(tool,True)

    # create yosys script
    lines  = get_inc_list(INC_DIR_LIST,prefix='read -incdir ')
    lines += ['read_verilog ' + s for s in get_source_files_alldir(SRC_DIR_LIST,fmts=['.v'])]

    lines.append('hierarchy -top %s' % TOPLEVEL)
    lines.append('write_verilog %s_full.v' % os.path.join(work_root,TOPLEVEL))
    if True:
        lines += ['synth']
    else:
        lines += ['synth_ice40']
    lines.append('write_verilog %s_synth.v' % os.path.join(work_root,TOPLEVEL))
    # lines += ['show -prefix ./ecdsa256 -format svg -viewer ']
    # lines += ['stat -tech xilinx']

    # print output
    ysoutfile = os.path.join(work_root,'%s.ys' % TOPLEVEL)
    write_file_lines(ysoutfile,lines,print_en=True)    

    # yosys command
    cmdstr = 'yosys -s %s > %s/yosys.log' % (ysoutfile,work_root)
    print(cmdstr)
    os.system(cmdstr)

    pass

if __name__ == '__main__':
    synth_yosys()