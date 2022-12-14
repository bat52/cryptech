#!/usr/bin/python3

SRC_DIR_LIST = [
    '../cryptech/cryptech_lib/memory',
    '../cryptech/cryptech_lib/multiword',
    '../cryptech/cryptech_lib/lowlevel/generic',
    '../cryptech/cryptech_lib/modular',
    '../cryptech/cryptech_ecdsalib/rtl/modular',
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