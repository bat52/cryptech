#!/usr/bin/env python3

import os
import shutil
import ast
import random
from pyeda.pyverilator import pyverilator_wrapper

from ecdsa256_common import *
from ecdsa256_tc import *

ECDSA256_NCYCLES_TIMEOUT=1e6

class dut_wrapper(pyverilator_wrapper):
    sim = None

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
        self.sim.io.cs = 1
        self.sim.clock.tick()

        # reset bus
        self.sim.io.address = 0
        self.sim.io.write_data = 0
        self.sim.io.we = 0
        self.sim.clock.tick()

    def reg_read(self,addr = '0x00'):

        if isinstance(addr,str):
            addr = ast.literal_eval(addr)

        # SW read
        self.sim.io.address = addr
        self.sim.io.we = 0
        self.sim.io.cs = 1
        self.sim.clock.tick()

        outval = self.sim.io.read_data

        self.sim.io.address = 0
        self.sim.clock.tick()

        # print(hex(outval))
        return outval

    def write_multi_word(self, baseaddr = 0, val = []):
        # write inputs
        for idx in range(len(val)):
            addr = baseaddr + idx
            # print("IDX: %d, ADDR: 0x%x, VAL: 0x%d" % (idx, addr, val[idx]))
            self.reg_write(addr, val[idx])
        pass

    def compare_multi_word(self, baseaddr = 0, val = [], assert_en = False):
        # read inputs
        for idx in range(len(val)):
            readval = self.reg_read(baseaddr + idx)
            
            if not(readval==val[idx]):
                print('Error! Index: %d, Read: 0x%08x, Expected: 0x%08x' % (idx, readval, val[idx]))

            if assert_en:
                assert(readval==val[idx])
        pass

    pass

class tb_test(dut_wrapper):

    def __init__(self, **kwargs):
        dut_wrapper.__init__(self, **kwargs)

        self.reset_release()

    def test_read_regs(self):

        print('Reading NAME0...')
        name0 = self.reg_read(ecdsa256regAddr.NAME0)
        assert(name0 == CORE_NAME0)

        print('Reading NAME1...')
        name1 = self.reg_read(ecdsa256regAddr.NAME1)
        assert(name1 == CORE_NAME1)

        print('Reading VERSION...')
        name1 = self.reg_read(ecdsa256regAddr.VERSION)
        assert(name1 == CORE_VERSION)

        print('W/R DUMMY...')
        for _ in range(3):
            rndval = random.randrange(1,ast.literal_eval('0xFFFFFFFF'))
            self.reg_write(ecdsa256regAddr.DUMMY,rndval)
            assert( self.reg_read(ecdsa256regAddr.DUMMY) == rndval )

        pass

    def test_ecdsa_point_mul(self,tc):
        # check inputs
        assert(isinstance(tc,ecdsaTc))

        # write input
        print('Writing K...')
        self.write_multi_word(ecdsa256regAddr.K, tc.k)

        print('Checking K...')
        self.compare_multi_word(ecdsa256regAddr.K, tc.k)

        print('Starting multiplication...')
        self.reg_write(ecdsa256regAddr.CONTROL,ecdsa256Control.en)

        print('Polling for multiplication done...')
        status = 1
        niterations = 0
        while (status < 3) and (niterations < ECDSA256_NCYCLES_TIMEOUT):
            status = self.reg_read(ecdsa256regAddr.STATUS)
            if (niterations % (ECDSA256_NCYCLES_TIMEOUT/10)) == 0:
                print('#%d, STATUS: %d' % (niterations,status) )
            niterations += 1

        print('#%d, STATUS: %d' % (niterations,status) )        
        print('Done!')

        print('Checking multiplication result QX...')
        self.compare_multi_word(ecdsa256regAddr.QX,tc.qx)
        print('Checking multiplication result QY...')
        self.compare_multi_word(ecdsa256regAddr.QY,tc.qy)
        print('Done!')

        self.reg_write(ecdsa256regAddr.CONTROL,0)
        pass

def pyverilate(dump_en = False):
    topfname = os.path.join(SRC_DIR_LIST[-1], TOPLEVEL+'.v')
    print(topfname)

    args = ["-Wno-TIMESCALEMOD", "-Wno-WIDTH", '--timescale-override', '1ns/1ns']
    tb = tb_test(fname = topfname,
                src_dirs= SRC_DIR_LIST+INC_DIR_LIST,
                command_args = args,
                dump_en=dump_en)

    tb.test_read_regs()

    if True:
        print("1. Q1 = d1 * G...")
        tb.test_ecdsa_point_mul(ECDSA_P256_NSA_TC1)
        
        print("2. R = k * G...")
        tb.test_ecdsa_point_mul(ECDSA_P256_NSA_TC2)
        
        print("3. Q2 = d2 * G...")
        tb.test_ecdsa_point_mul(ECDSA_P256_RANDOM)
        
        print("4. O = n * G...")
        tb.test_ecdsa_point_mul(ECDSA_P256_O)
        
        print("5. G = (n + 1) * G...")
        tb.test_ecdsa_point_mul(ECDSA_P256_G)

        print("6. H = 2 * G...")
        tb.test_ecdsa_point_mul(ECDSA_P256_H)
        
        print("7. H = (n + 2) * G...")
        tb.test_ecdsa_point_mul(ECDSA_P256_H2)

    pass

if __name__ == '__main__':
    pyverilate()