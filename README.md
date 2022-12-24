# cryptech

This repository uses the [cryptech](https://cryptech.is/) [ECDSA256 Scalar Point Multiplier](https://git.cryptech.is/core/pkey/ecdsa256/) to test [edalize](https://github.com/olofk/edalize).
Currently testbench simulation works using [Icarus Verilog](http://iverilog.icarus.com/).
Initial work to support synthesis with [trellis](https://github.com/YosysHQ/prjtrellis) and [yosys](https://yosyshq.net/yosys/) has been done, but does not work yet.

# usage

    cd pycryptech
    ./ecdsa256.py --help           # simulation
                                   # synthesis with yosys/trellis (not working yet)
    ./ecdsa256_siliconcompiler.py  # backend flow with siliconcompiler (not working yet)
  
