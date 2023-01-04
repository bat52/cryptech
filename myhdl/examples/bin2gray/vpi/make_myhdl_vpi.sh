#!/usr/bin/env bash

URL=https://raw.githubusercontent.com/myhdl/myhdl/master/cosimulation/icarus
wget ${URL}/myhdl.c
wget ${URL}/myhdl_table.c
wget ${URL}/Makefile
make