#!/usr/bin/env bash
# cd ./vpi && ./make.sh && make && cd ..
iverilog -o bin2gray -DDUMP_EN=1 -DDUMP_LEVEL=0 -DDUMP_MODULE=dut -Dwidth=4 bin2gray.v dut_bin2gray.v # manual tb
# iverilog -o bin2gray -Dwidth=4 bin2gray.v tb_bin2gray.v # use auto-generated tb
# vvp -m ./vpi/myhdl.vpi bin2gray # just test