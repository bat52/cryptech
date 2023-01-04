#!/usr/bin/env python3

import os

from myhdl import *
from bin2gray import bin2gray_myhdl, bin2gray_rtl

@block
def clk_driver(clk, period=10):
    ''' Clock driver '''
    @always(delay(period//2))
    def driver():
        clk.next = not clk

    return driver

@block
def tb_bin2gray(width=4, cosim=False):
    b = Signal(intbv(0)[width:])
    g = Signal(intbv(0)[width:])
    en = Signal(bool(1))
    clk = Signal(bool(0))
    resetn = ResetSignal(1, active=0, isasync=True)

    if not(cosim):
        dut = bin2gray_myhdl(b,g, en)
    else:
        dut = bin2gray_rtl(b,g, en)

    clk_driver_i = clk_driver(clk)

    @always_seq(clk.posedge,resetn)
    def count():
        if b<14:
            b.next=b+1
        else:
            b.next=0

    return instances()

def view(fname):
    os.system('gtkwave %s &' % fname)

if __name__ == '__main__':

    cosim = True
    duration = 200

    os.system('rm *.vcd')

    tb = tb_bin2gray(cosim=cosim)        

    if not(cosim):
        if False:
            # this also works
            sim = Simulation(traceSignals(tb))        
            sim.run(duration)
        else:   
            tb.config_sim(trace=True)
            tb.run_sim(duration)
        view('tb_bin2gray.vcd')
    else:
        # myhdl dump does not work,
        # need to simulate like this, 
        # and dump in verilog side
        sim = Simulation(tb)        
        sim.run(duration)   
        view('dump.vcd')
    