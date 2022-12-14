#!/usr/bin/env python3

import os
import shutil
import ast
import pyverilator

from ecdsa256_common import *

class pyverilator_wrapper():
    sim = None

    def __init__(self, fname='', verilog_path=[], command_args = []):

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

        # start gtkwave to view the waveforms as they are made
        self.sim.start_gtkwave()

        # add all the io and internal signals to gtkwave
        # sim.send_signal_to_gtkwave(sim.io)
        # sim.send_signal_to_gtkwave(sim.internals)

        # add all the io and internal signals to gtkwave
        self.sim.send_to_gtkwave(self.sim.io)
        self.sim.send_to_gtkwave(self.sim.internals)

        self.reset_release()

    def reset_release(self):
        # tick the automatically detected clock
        self.sim.clock.tick()

        # set rst back to 0
        # sim.io.rst = 0
        self.sim.io.reset_n = 0
        self.sim.clock.tick()
        self.sim.io.reset_n = 1

    def reg_write(self, addr='0x00', val='0x00000000'):

        if isinstance(addr,str):
            addr = ast.literal_eval(addr)

        if isinstance(val,str):
            val = ast.literal_eval(val)

        if isinstance(mask,str):
            mask = ast.literal_eval(mask)

        # write value        
        self.sim.io.address = addr
        self.sim.io.write_data = val
        self.sim.io.read_data = 0
        self.sim.io.we = 1
        self.sim.io.cs = 0

        self.sim.clock.tick()

        self.sim.io.cs = 1

        self.sim.clock.tick()

        # reset bus
        self.sim.io.address = 0
        self.sim.io.write_data = 0
        self.sim.io.read_data = 0
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

def pyverilate():
    topfname = os.path.join(SRC_DIR_LIST[-1], TOPLEVEL+'.v')
    print(topfname)

    # args = ["--timescale-override 1ns/1ps"]
    args = ["-Wno-TIMESCALEMOD", "-Wno-WIDTH"]
    # --top-module <topname>      Name of top level input module
    tb = pyverilator_wrapper(fname = topfname,
                             verilog_path = SRC_DIR_LIST+INC_DIR_LIST,
                             command_args = args)
    pass