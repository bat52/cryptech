#include <stdlib.h>
#include <iostream>
#include <verilated.h>
#if VM_TRACE
#include <verilated_vcd_c.h>
#endif
// 
#include "Vecdsa256_wrapper.h"

#define MAX_SIM_TIME 78e3 // 78ms on original tb 
vluint64_t sim_time = 0;


// Registers  
#define ADDR_NAME0      0
#define ADDR_NAME1      1
#define ADDR_VERSION    2

#define ADDR_CONTROL    8   // {next, init}
#define ADDR_STATUS     9   // {valid, ready}
#define ADDR_DUMMY      15  // don't care

// Y = k*X
// -------
// K-coefs
// 0x0080 | K0 
// 0x0084 | K1 
// ... 
// 0x009C | K7
//
// X-coefs
// 0x00A0 | X0 
// 0x00A4 | X1 
// ... 
// 0x00BC | X7 
//
// Y-coefs// 0x00C0 | Y0 
// 0x00C4 | Y1 
// ... 
// 0x00DC | Y7

// Bitfields
// #define CONTROL_INIT_BIT  = 0; -- not used
#define CONTROL_NEXT_BIT  = 1;

// #define STATUS_READY_BIT  = 0; -- hardcoded to always read 1
#define STATUS_VALID_BIT  = 1;

#define CORE_NAME0    0x65636473 // "ecds"
#define CORE_NAME1    0x61323536 // "a256"
#define CORE_VERSION  0x302E3230 // "0.20"

void test_reg_name(Vecdsa256_wrapper *dut){
    static uint posedge_counter = 0;

    if (dut->clk == 1)
        posedge_counter++;

    dut->cs = 1; // chip select
    
    switch(posedge_counter){
        case 2:
            std::cout << "TESTING REGISTER NAME0...\n";
            dut->address = ADDR_NAME0;
            break;
        case 3:
            if( dut->read_data != CORE_NAME0 )
                std::cout << "ERROR!!! REGISTER NAME0 VALUE:" << std::hex << (dut->read_data) << '\n';
            break;
        case 4:
            std::cout << "TESTING REGISTER NAME1...\n";
            dut->address = ADDR_NAME1;
            break;
        case 5:
            if( dut->read_data != CORE_NAME1 )
                std::cout << "REGISTER NAME1 VALUE:" << std::hex << (dut->read_data) << '\n';
            break;
    }

}

int main(int argc, char** argv, char** env) {
    Vecdsa256_wrapper *dut = new Vecdsa256_wrapper;

#if VM_TRACE
    Verilated::traceEverOn(true);
    VerilatedVcdC *m_trace = new VerilatedVcdC;

    dut->trace(m_trace, 5);
    m_trace->open("dump.vcd");
#endif

    dut->reset_n = 0; // reset
    while (sim_time < MAX_SIM_TIME) {
        if(sim_time > 1 && sim_time < 5 )
            dut->reset_n = 1; // release reset

        test_reg_name(dut);

        dut->clk ^= 1;
        dut->eval();
#if VM_TRACE
        m_trace->dump(sim_time);
#endif
        sim_time++;
    }

#if VM_TRACE
    m_trace->close();
#endif
    delete dut;
    exit(EXIT_SUCCESS);
}