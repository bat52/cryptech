#include <stdlib.h>
#include <iostream>
#include <verilated.h>
#if VM_TRACE
#include <verilated_vcd_c.h>
#endif
// 
#include "Vecdsa256_wrapper.h"

// Registers  
#define ADDR_NAME0      0
#define ADDR_NAME1      1
#define ADDR_VERSION    2

#define ADDR_CONTROL    8   // {next, init}
#define ADDR_STATUS     9   // {valid, ready}
#define ADDR_DUMMY      15  // don't care

#define ADDR_K          0x20
#define ADDR_QX         0x28
#define ADDR_QY         0x30

// Bitfields
// #define CONTROL_INIT_BIT  = 0; -- not used
#define CONTROL_NEXT_BIT  = 1;

// #define STATUS_READY_BIT  = 0; -- hardcoded to always read 1
#define STATUS_VALID_BIT  = 1;

#define CORE_NAME0    0x65636473 // "ecds"
#define CORE_NAME1    0x61323536 // "a256"
#define CORE_VERSION  0x302E3230 // "0.20"

#define NWORDS_ECDSA256 8
#define ECDSA256_NCYCLES_TIMEOUT 1000000

const uint32_t ECDSA_P256_D_NSA[NWORDS_ECDSA256] =
	{0x3452b38a, 0x9f2d7d5b, 0x851bf634, 0x3f04d7d6,
	 0xc21a472b, 0x56ff68cf, 0xb16845ed, 0x70a12c2d};
/*
	{0x70a12c2d, 0xb16845ed, 0x56ff68cf, 0xc21a472b,
	 0x3f04d7d6, 0x851bf634, 0x9f2d7d5b, 0x3452b38a};
*/

const uint32_t ECDSA_P256_QX_NSA[NWORDS_ECDSA256] =
	{0xf26680a8, 0xf7635eaf, 0x2d22cba4, 0x8691a326,
	 0x6e2bd3d8, 0xd70cf69a, 0x7464a6ea, 0x8101ece4};
/*    {0x8101ece4, 0x7464a6ea, 0xd70cf69a, 0x6e2bd3d8,
	 0x8691a326, 0x2d22cba4, 0xf7635eaf, 0xf26680a8};
     */
	 
const uint32_t ECDSA_P256_QY_NSA[NWORDS_ECDSA256] =
	{0x36c0c3a9, 0xa6240799, 0x8f0a5aba, 0xd3ca43e7,
	 0xd58f1783, 0xf67d9cb4, 0x1d599235, 0xd8a12ba6};
     /*{0xd8a12ba6, 0x1d599235, 0xf67d9cb4, 0xd58f1783,
	 0xd3ca43e7, 0x8f0a5aba, 0xa6240799, 0x36c0c3a9};*/

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

void DutWrapper::check_reg_val(uint32_t addr, uint32_t val)
{
    uint32_t readval;
    readval = this->reg_read( addr );
    if ( readval != val )
        {
        std::cout << "ERROR!!! REGISTER 0x" << std::hex << (addr)
        << " VALUE: " << std::hex << (readval) << '\n';
        }
}

void DutWrapper::write_multi_word(uint32_t baseaddr, uint32_t *val)
{
    int idx; 
    for (idx=0; idx < NWORDS_ECDSA256; idx++)
        this->reg_write(baseaddr + idx, val[idx]);
}

void DutWrapper::compare_multi_word(uint32_t baseaddr, uint32_t *val)
{
    int idx;
    // read inputs
    for( idx=0; idx < NWORDS_ECDSA256; idx++)
        this->check_reg_val(baseaddr + idx, val[idx]);
}

class DutTest : public DutWrapper{
    public:
        void test_read_registers();
        void test_rw_registers();
        void test_ecdsa_point_mul(const uint32_t *k, const uint32_t *qx, const uint32_t *qy);
};

void DutTest::test_read_registers(){

    this->check_reg_val(ADDR_NAME0, CORE_NAME0);
    this->check_reg_val(ADDR_NAME1, CORE_NAME1);
    this->check_reg_val(ADDR_VERSION, CORE_VERSION);
}

void DutTest::test_rw_registers(){
    int ii, val;

    for (ii=0; ii < 32; ii++)
        {
            val = 1 << ii;
            this->reg_write(ADDR_DUMMY, val);
            this->check_reg_val(ADDR_DUMMY, val);
        }
}

void DutTest::test_ecdsa_point_mul(const uint32_t *k, const uint32_t *qx, const uint32_t *qy){

    uint32_t status = 1;
    int niterations = 0;

    this->write_multi_word(ADDR_K, (uint32_t *) k);
    this->compare_multi_word(ADDR_K, (uint32_t *)k);

    status = this->reg_read(ADDR_STATUS);
    std::cout << " STATUS: " << status << '\n';

    this->reg_write(ADDR_CONTROL,0);
    this->reg_write(ADDR_CONTROL,3); // give one extra clock cycle
    this->reg_read(ADDR_CONTROL); // give one extra clock cycle
    
    status = this->reg_read(ADDR_STATUS);
    std::cout << " STATUS: " << status << '\n';

    while ((status < 3) && (niterations < ECDSA256_NCYCLES_TIMEOUT))
        {
        niterations++;
        status = this->reg_read(ADDR_STATUS);

        if ((niterations % 100000) == 0)
            std::cout << "#ITERATIONS: " << niterations << " STATUS: " << status << '\n';
        }

    std::cout << "#ITERATIONS: " << niterations << " STATUS: " << status << '\n';

    this->compare_multi_word(ADDR_QX,(uint32_t *)qx);
    this->compare_multi_word(ADDR_QY,(uint32_t *)qy);

    this->reg_write(ADDR_CONTROL,0);
}

int main(int argc, char** argv, char** env) {
    DutTest *dut = new DutTest;

    // dut->test_read_registers();
    // dut->test_rw_registers();
    dut->test_ecdsa_point_mul(ECDSA_P256_D_NSA, ECDSA_P256_QX_NSA, ECDSA_P256_QY_NSA );
    
    delete dut;
    exit(EXIT_SUCCESS);
}