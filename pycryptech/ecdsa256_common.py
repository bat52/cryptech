#!/usr/bin/python3

from enum import IntEnum

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

## Registers ##

CORE_NAME0   = 0x65636473 # "ecds"
CORE_NAME1   = 0x61323536 # "a256"
CORE_VERSION = 0x302E3230 # "0.20"

class ecdsa256regAddr(IntEnum):
    NAME0   = 0
    NAME1   = 1
    VERSION = 2
    CONTROL = 8
    STATUS  = 9
    DUMMY   = 15
    K       = 0b1_00_000 # 0x20
    QX      = 0b1_01_000 # 0x28
    QY      = 0b1_10_000 # 0x30

class ecdsa256Control(IntEnum):
    en = 2