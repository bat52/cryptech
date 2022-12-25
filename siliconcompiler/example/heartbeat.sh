#!/usr/bin/env bash
# override yosys with oss cad suite
OSS_BIN_DIR=/media/marco/DATA/programming/rtl/oss-cad-suite-linux-x64-20221224/oss-cad-suite/bin
PATH=$OSS_BIN_DIR:$PATH
export SCPATH=../siliconcompiler/siliconcompiler
rm -rf ./build
./heartbeat.py $@