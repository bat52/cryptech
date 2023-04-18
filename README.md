# cryptech

This repository uses the [cryptech](https://cryptech.is/) [ECDSA256 Scalar Point Multiplier](https://git.cryptech.is/core/pkey/ecdsa256/) to test various EDA tools, including [edalize](https://github.com/olofk/edalize), [verilator](https://www.veripool.org/verilator/) and [siliconcompiler](https://www.siliconcompiler.com/).

Currently testbench simulations work using:
- [Icarus Verilog](http://iverilog.icarus.com/).
- [pyverilator](https://pypi.org/project/PyVerilator/): note this requires some [minor fixes](https://github.com/csail-csg/pyverilator/issues/16) that are not available in the pyverilator version published through pypi.
- verilator through edalize

Currently synthesys and gate count work using [yosys](https://yosyshq.net/yosys/) standalone and with edalize.
Possibly [trellis](https://github.com/YosysHQ/prjtrellis), works too but the full flow has not been tested yet.
Initial work to support [siliconcompiler](https://www.siliconcompiler.com/) has been done, and seems to [work in remote mode](https://www.linkedin.com/feed/update/urn:li:activity:7044353070171869185?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A7044353070171869185%2C7045769771736276992%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287045769771736276992%2Curn%3Ali%3Aactivity%3A7044353070171869185%29).

# usage

    cd pycryptech
    ./ecdsa256_main.py --help           # simulation
    ./ecdsa256_main.py -sim icarus      # simulation with icarus
    ./ecdsa256_main.py -sim pyverilator # simulation with pyverilator
    ./ecdsa256_main.py -sim verilator   # simulation with verilator
    ./ecdsa256_main.py -synth yosys     # synthesis with yosys
    ./ecdsa256_main.py -synth sc        # backend flow with siliconcompiler (not working yet)
  
