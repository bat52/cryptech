#!/usr/bin/env bash
export SCPATH=../siliconcompiler/siliconcompiler
rm -rf ./build
./siliconcompiler_wrapper.py $@