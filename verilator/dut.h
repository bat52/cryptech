#include <stdint.h> 

void dut_init();
void dut_close();

uint32_t reg_read(uint32_t addr);
void reg_write(uint32_t addr, uint32_t val);



