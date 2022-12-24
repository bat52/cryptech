#include <stdlib.h>
#include <iostream>
#include <verilated.h>

#if VM_TRACE
    #ifdef DUMP_FST
        #include <verilated_fst_c.h>
        #define DUMP_TYPE VerilatedFstC
        #define DUMP_FILE "dump.fst"
    #else
        #include <verilated_vcd_c.h>
        #define DUMP_TYPE VerilatedVcdC
        #define DUMP_FILE "dump.vcd"
    #endif
#endif
#include "Vecdsa256_wrapper.h"

#ifndef CLK_HALF_PERIOD_DELAY
#define CLK_HALF_PERIOD_DELAY 5
#endif

#ifndef DUMP_LEVEL
#define DUMP_LEVEL 0
#endif

class DutWrapper : public Vecdsa256_wrapper{
    public: 
        vluint64_t sim_time = 0;
        DutWrapper();
        ~DutWrapper();

        void release_reset();
        void reg_write(uint32_t addr, uint32_t val);
        uint32_t reg_read(uint32_t addr);

    private:
        #if VM_TRACE    
        DUMP_TYPE *m_trace;
        #endif
        void half_clock_tick();
        void clock_tick();
};

void DutWrapper::half_clock_tick()
{
    this->clk ^= 1;
    this->eval();
#if VM_TRACE
    this->m_trace->dump(sim_time);
#endif
    this->sim_time += CLK_HALF_PERIOD_DELAY;
}

void DutWrapper::clock_tick()
{
    this->half_clock_tick();
    this->half_clock_tick();
}

void DutWrapper::release_reset()
{
    this->address = 0;
    this->write_data = 0;
    this->we = 0;
    this->cs = 0;

    this->reset_n = 0; // reset
    this->clock_tick();
    this->half_clock_tick(); // asynchronous

    this->reset_n = 1;
    this->clock_tick();
    this->clock_tick();

}

DutWrapper::DutWrapper()
{
    #if VM_TRACE
        Verilated::traceEverOn(true);
        this->m_trace = new DUMP_TYPE;
        this->trace(this->m_trace, DUMP_LEVEL);
        this->m_trace->open(DUMP_FILE);
    #endif

    this->release_reset();
}

DutWrapper::~DutWrapper()
{
#if VM_TRACE
    m_trace->close();
    delete m_trace;
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

    outval = this->read_data;

    // reset bus
    this->address = 0;
    this->cs = 0;
    this->clock_tick();

    return outval;
}        

/////////////// C-style access

DutWrapper *dut;

void dut_init(){
    dut = new DutWrapper;
}

void dut_close(){
    delete dut;
}

uint32_t reg_read(uint32_t addr)
{
    return dut->reg_read(addr);
}

void reg_write(uint32_t addr, uint32_t val)
{
    dut->reg_write(addr,val);
}
