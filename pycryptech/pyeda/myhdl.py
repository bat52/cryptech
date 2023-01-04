#!/usr/bin/env python3

import os
from pyeda.edalize import icarus
from pyeda.common import get_clean_work, vcd_view
import veriloggen as vg
from myhdl import *

def top2wrapper(topfile, topmodule,  filename='dut_wrapper.v', dump_en = False):

    modules = vg.from_verilog.read_verilog_module(topfile)
    top = modules[topmodule]   # dut real instance

    wrapper_name = os.path.basename(filename).split('.')[0]

    m = vg.Module(wrapper_name) # dut wrapper instance
    d = vg.StubModule(top.name) # dut stub instance
    dump = vg.StubModule('dump') # dumper module

    instlist = {}
    input_list = {}
    output_list = {}
    for io,iotype in top.io_variable.items():

        if isinstance(iotype,vg.core.vtypes.Input):            
            input_list[io] = instlist[io] = m.Reg(name=io, width=iotype.width)

        elif isinstance(iotype,vg.core.vtypes.Output):            
            output_list[io] = instlist[io] = m.Wire(name=io, width=iotype.width)
        else:
            assert(False)

    fromlist = input_list.values()
    # print(*fromlist)
    tolist = output_list.values()

    instlist['from_myhdl']  = m.Initial( vg.Systask('from_myhdl', *fromlist ) )
    instlist['to_myhdl']    = m.Initial( vg.Systask(  'to_myhdl', *tolist) )

    # copy paras and ports
    ports = {**input_list,**output_list}
    print(ports)
    dut = m.Instance(d, 'dut', ports=ports)

    if dump_en:
        dump_i = m.Instance(dump, 'localdump')

    m.to_verilog(filename=filename)
    return wrapper_name

def top2signals(topfile='', topmodule=''):

    modules = vg.from_verilog.read_verilog_module(topfile)
    top = modules[topmodule]   # dut real instance

    slist = {}    
    for io,iotype in top.io_variable.items():

        if (isinstance(iotype,vg.core.vtypes.Input) or
            isinstance(iotype,vg.core.vtypes.Output)):
            slist[io] = Signal(intbv(0)[iotype.width:])

    return slist

def cosim_make_stub(topfile='',topmodule='',filename='dut_wrapper.v', dump_en=False):

    tool = 'myhdl'
    work = get_clean_work(tool=tool,makedir=True)
    full_file = os.path.join(work,filename)

    wrapper = top2wrapper(topfile=topfile, topmodule=topmodule, filename=full_file, dump_en=dump_en)

    return work, wrapper #, full_file

def cosimulation(vpi_path='./work_myhdl_vpi', vpi='myhdl', dut='', work='./work_icarus', ports={}):
    cmdstr = 'vvp -M %s -m%s %s' % (vpi_path, vpi, dut)
    
    os.chdir(work)
    print(cmdstr)
    return Cosimulation( cmdstr, **ports )

def myhdl_cosim_dut(topmodule='', topfile='',dump_en=False, ports={},
    simname ='', src_dirs=[],inc_dirs=[]):
    work, wrapper = cosim_make_stub(topfile=topfile,topmodule=topmodule, dump_en=dump_en)

    # build dut
    print('##### Building icarus...')
    icarus_inst = icarus(
        simname=simname,
        top=wrapper,
        src_dirs = src_dirs + [work],
        inc_dirs = inc_dirs,
        dump_en=dump_en,
        myhdl_en = True,
        run_en=False)
    print('##### Building icarus... Done')

    # cosimulation
    return [ cosimulation(vpi_path=icarus_inst['mvpi'].work, 
                        work=icarus_inst['work_root'],
                        dut=simname, ports=ports),
            icarus_inst['work_root']]

@block
def clk_driver(clk, period=10):
    ''' Clock driver '''
    @always(delay(period//2))
    def driver():
        clk.next = not clk
    return driver

def myhdl_cosim_tb(topfile='',topmodule='',simname='',src_dirs=[], inc_dirs=[],dump_en=False,
    clock='clk'):

    ports = top2signals(topfile=topfile, topmodule=topmodule)
    dut,work = myhdl_cosim_dut(topfile=topfile, topmodule=topmodule, ports=ports,
        simname=simname,src_dirs=src_dirs,inc_dirs=inc_dirs, dump_en=dump_en)

    clk_driver_i = clk_driver(ports[clock])

    return {'sim': instances(), 'io': ports, 'work': work }
    # return instances()

class myhdl_wrapper(object):
    sim = None
    io = None
    clock = 'clk'
    reset = 'resetn'

    def __init__(self, fname='', src_dirs=[], inc_dirs=[], simname='', dump_en = False, duration=200):
        topmodule,ext = os.path.splitext(os.path.basename(fname))

        tb = myhdl_cosim_tb(topfile=fname, topmodule=topmodule, simname=simname,
                src_dirs=src_dirs, inc_dirs=inc_dirs, dump_en=dump_en) 

        self.sim = Simulation( tb['sim'] )        
        self.io  = tb['io']

        #### run simulation
        self.sim.run(duration)
        if dump_en:
            vcd_view(os.path.join(tb['work'], 'dump.vcd'),postcmd='&')
        pass

