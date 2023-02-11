# cryptech

This repository uses the [cryptech](https://cryptech.is/) [ECDSA256 Scalar Point Multiplier](https://git.cryptech.is/core/pkey/ecdsa256/) to test various EDA tools, including [edalize](https://github.com/olofk/edalize), [verilator](https://www.veripool.org/verilator/) and [siliconcompiler](https://www.siliconcompiler.com/).

Currently testbench simulations work using:
- [Icarus Verilog](http://iverilog.icarus.com/).
- [pyverilator](https://pypi.org/project/PyVerilator/): note this requires some [minor fixes](https://github.com/csail-csg/pyverilator/issues/16) that are not available in the pyverilator version published through pypi.
- verilator through edalize

Currently synthesys and gate count work using [yosys](https://yosyshq.net/yosys/).

Initial work to support synthesis through edalize with [trellis](https://github.com/YosysHQ/prjtrellis), [yosys](https://yosyshq.net/yosys/) and [siliconcompiler](https://www.siliconcompiler.com/) has been done, but [does not work](https://github.com/siliconcompiler/siliconcompiler/discussions/1179) yet.

# usage

    cd pycryptech
    ./ecdsa256_main.py --help           # simulation
    ./ecdsa256_main.py -sim icarus      # simulation with icarus
    ./ecdsa256_main.py -sim pyverilator # simulation with pyverilator
    ./ecdsa256_main.py -sim verilator   # simulation with verilator
    ./ecdsa256_main.py -synth yosys     # synthesis with yosys
    ./ecdsa256_siliconcompiler.py  # backend flow with siliconcompiler (not working yet)
  
