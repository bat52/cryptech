#!/usr/bin/env python3

import os
import shutil
import ast
import random
import pyverilator

from ecdsa256_common import *
from ecdsa256_tc import *

ECDSA256_NCYCLES_TIMEOUT=1e6

class pyverilator_wrapper(object):
    sim = None

    def __init__(self, fname='', verilog_path=[], command_args = [], wave_en = False):

        # rename to .v, if .sv
        if not os.path.isfile(fname):
            print('File %s does not exist!' % fname)
            assert(False)

        base,ext = os.path.splitext(fname)
        # print(ext)

        if ext == '.sv':
            print('renaming input file to .v')
            ofname = base + '.v'
            shutil.copyfile(fname, ofname)
        else:
            ofname = fname

        print(ofname)
        self.sim = pyverilator.PyVerilator.build(ofname, 
                                                 verilog_path=verilog_path, 
                                                 command_args=command_args) # command_args not passed to verilator with pyverilator 0.7.0
        if wave_en:
            self.view_waves()

        self.reset_release()

    def view_waves(self):
        # start gtkwave to view the waveforms as they are made
        self.sim.start_gtkwave()

        # add all the io and internal signals to gtkwave
        self.sim.send_to_gtkwave(self.sim.io)
        self.sim.send_to_gtkwave(self.sim.internals)

    def reset_release(self):
        # tick the automatically detected clock
        self.sim.clock.tick()

        # set rst back to 0
        # sim.io.rst = 0
        self.sim.io.reset_n = 0
        self.sim.clock.tick()
        self.sim.io.reset_n = 1

    def reg_write(self, addr='0x00', val='0x00000000', mask = '0xFFFFFFFF'):

        if isinstance(addr,str):
            addr = ast.literal_eval(addr)

        if isinstance(val,str):
            val = ast.literal_eval(val)

        if isinstance(mask,str):
            mask = ast.literal_eval(mask)

        # write value        
        self.sim.io.address = addr
        self.sim.io.write_data = val
        self.sim.io.we = 1
        self.sim.io.cs = 0

        self.sim.clock.tick()

        self.sim.io.cs = 1

        self.sim.clock.tick()

        # reset bus
        self.sim.io.address = 0
        self.sim.io.write_data = 0
        self.sim.io.cs = 0
        self.sim.io.we = 0

        self.sim.clock.tick()

    def reg_read(self,addr = '0x00'):

        if isinstance(addr,str):
            addr = ast.literal_eval(addr)

        # SW read
        self.sim.io.address = addr
        self.sim.io.we = 0
        self.sim.io.cs = 0
        self.sim.clock.tick()

        self.sim.io.cs = 1
        self.sim.clock.tick()

        outval = self.sim.io.read_data

        self.sim.io.address = 0
        self.sim.io.cs = 0
        self.sim.clock.tick()

        # print(hex(outval))
        return outval

    def write_multi_word(self, baseaddr = 0, val = []):
        # write inputs
        for idx in range(len(val)):
            self.reg_write(baseaddr + 4*idx, val[idx])
        pass

    def compare_multi_word(self, baseaddr = 0, val = [], assert_en = False):
        # read inputs
        for idx in range(len(val)):
            readval = self.reg_read(baseaddr + 4*idx)
            
            if not(readval==val[idx]):
                print('Error! Index: %d, Read: 0x%08x, Expected: 0x%08x' % (idx, readval, val[idx]))

            if assert_en:
                assert(readval==val[idx])
        pass

    pass

def test_read_regs(tb):
    assert(isinstance(tb,pyverilator_wrapper))

    print('Reading NAME0...')
    name0 = tb.reg_read(ecdsa256regAddr.NAME0)
    assert(name0 == CORE_NAME0)

    print('Reading NAME1...')
    name1 = tb.reg_read(ecdsa256regAddr.NAME1)
    assert(name1 == CORE_NAME1)

    print('Reading VERSION...')
    name1 = tb.reg_read(ecdsa256regAddr.VERSION)
    assert(name1 == CORE_VERSION)

    print('W/R DUMMY...')
    for _ in range(3):
        rndval = random.randrange(1,ast.literal_eval('0xFFFFFFFF'))
        tb.reg_write(ecdsa256regAddr.DUMMY,rndval)
        assert( tb.reg_read(ecdsa256regAddr.DUMMY) == rndval )

    pass

def test_ecdsa_point_mul(tb,tc):
    # check inputs
    assert(isinstance(tb,pyverilator_wrapper))
    assert(isinstance(tc,ecdsaTc))

    # write input
    print('Writing K...')
    tb.write_multi_word(ecdsa256regAddr.K, tc.k)

    print('Checking K...')
    tb.compare_multi_word(ecdsa256regAddr.K, tc.k)

    print('Starting multiplication...')
    tb.reg_write(ecdsa256regAddr.CONTROL,2)

    print('Polling for multiplication done...')
    status = 1
    niterations = 0
    while (status < 3) and (niterations < ECDSA256_NCYCLES_TIMEOUT):
        status = tb.reg_read(ecdsa256regAddr.STATUS)
        if (niterations % (ECDSA256_NCYCLES_TIMEOUT/10)) == 0:
            print('#%d, STATUS: %d' % (niterations,status) )
        niterations += 1
    print('Done!')

    # tb.reg_write(ecdsa256regAddr.CONTROL,0)

    print('Checking multiplication result QX...')
    tb.compare_multi_word(ecdsa256regAddr.QX,tc.qx)
    print('Checking multiplication result QY...')
    tb.compare_multi_word(ecdsa256regAddr.QY,tc.qy)
    print('Done!')

    pass

def pyverilate():
    topfname = os.path.join(SRC_DIR_LIST[-1], TOPLEVEL+'.v')
    print(topfname)

    args = ["-Wno-TIMESCALEMOD", "-Wno-WIDTH"]
    tb = pyverilator_wrapper(fname = topfname,
                             verilog_path = SRC_DIR_LIST+INC_DIR_LIST,
                             command_args = args)

    test_read_regs(tb)
    test_ecdsa_point_mul(tb,ECDSA_P256_NSA_TC1)

    pass