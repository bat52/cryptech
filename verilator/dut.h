#include <stdlib.h> 
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

/*
DutWrapper *dut;
uint32_t reg_read(uint32_t addr);
void reg_write(uint32_t addr, uint32_t val);
*/


