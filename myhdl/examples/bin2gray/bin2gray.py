#!/usr/bin/env python3

import os
from myhdl import *

@block
def bin2gray_myhdl(B, G):
    """ Gray encoder.

    B -- binary input 
    G -- Gray encoded output
    """

    @always_comb
    def logic():
        G.next = (B>>1) ^ B

    return logic

def bin2gray_to_verilog(width=4):
    b = Signal(intbv(0)[width:])
    g = Signal(intbv(0)[width:])

    dut = bin2gray_myhdl(b,g)
    dut.convert()

cmd = "iverilog -o bin2gray.o -Dwidth=%s " + \
      "-DDUMP_EN=1 -DDUMP_LEVEL=0 -DDUMP_MODULE=dut " + \
      "bin2gray.v " + \
      "dut_bin2gray.v "

def bin2gray_rtl(B, G, EN):
    width = len(B)
    cmdstr = cmd % width
    print(cmdstr)
    os.system(cmdstr)
    return Cosimulation("vvp -m ./vpi/myhdl.vpi bin2gray.o", B=B, G=G, EN=EN)

if __name__ == '__main__':
    bin2gray_to_verilog()
    