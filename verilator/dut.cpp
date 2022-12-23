#include <stdlib.h>
#include <iostream>
#include <verilated.h>
#if VM_TRACE
#include <verilated_vcd_c.h>
#endif
// 
#include "Vecdsa256_wrapper.h"

class DutWrapper : public Vecdsa256_wrapper{
    public: 
        vluint64_t sim_time = 0;
        DutWrapper();
        ~DutWrapper();
        void reg_write(uint32_t addr, uint32_t val);
        uint32_t reg_read(uint32_t addr);
        void check_reg_val(uint32_t addr, uint32_t val);
        void write_multi_word(uint32_t baseaddr, uint32_t *val);
        void compare_multi_word(uint32_t baseaddr, uint32_t *val);
    private:
        void clock_tick();
#if VM_TRACE    
        VerilatedVcdC *m_trace = new VerilatedVcdC;
#endif
};

void DutWrapper::clock_tick()
{
    this->clk ^= 1;
    this->eval();
#if VM_TRACE
    this->m_trace->dump(sim_time);
#endif
    this->sim_time++;
}

DutWrapper::DutWrapper()
{
    #if VM_TRACE
    Verilated::traceEverOn(true);
    // this->m_trace = new VerilatedVcdC;

    this->trace(this->m_trace, 5);
    this->m_trace->open("dump.vcd");
    #endif

    this->address = 0;
    this->write_data = 0;
    this->we = 0;
    this->cs = 0;

    this->reset_n = 0; // reset
    this->clock_tick();
    this->clock_tick();

    this->reset_n = 1;
    this->clock_tick();
    this->clock_tick();
}

DutWrapper::~DutWrapper()
{
#if VM_TRACE
    m_trace->close();
#endif
}

void DutWrapper::reg_write(uint32_t addr, uint32_t val)
{
    // write value        
    this->address = addr;
    this->write_data = val;
    this->we = 1;
    this->cs = 1;
    this->clock_tick();

    // reset bus
    this->address = 0;
    this->write_data = 0;
    this->we = 0;
    this->cs = 0;
    this->clock_tick();
}

uint32_t DutWrapper::reg_read(uint32_t addr)
{
    uint32_t outval;
    // SW read
    this->address = addr;
    this->we = 0;
    this->cs = 1;
    this->clock_tick();

    // reset bus
    // this->address = 0;
    // this->cs = 0;
    // this->clock_tick();

    outval = this->read_data;

    this->address = 0;
    this->cs = 0;
    this->clock_tick();

    return outval;
}        

/////////////// C-style access

DutWrapper *dut = new DutWrapper;
uint32_t reg_read(uint32_t addr)
{
    return dut->reg_read(addr);
}

void reg_write(uint32_t addr, uint32_t val)
{
    dut->reg_write(addr,val);
}
