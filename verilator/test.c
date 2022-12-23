
#include <stdio.h>
#include "dut.h"
#include "ecdsa256_hal.h"
#include "ecdsa256_test_vectors.h"

////////// DUT functions extensions //////////////////////////////

void check_reg_val(uint32_t addr, uint32_t val)
{
    uint32_t readval;
    readval = reg_read( addr );
    if ( readval != val )
        printf("ERROR!!! REGISTER: 0x%08x, VALUE: 0x%08x\n", addr, readval);
}

void write_multi_word(uint32_t baseaddr, uint32_t *val)
{
    int idx; 
    for (idx=0; idx < NWORDS_ECDSA256; idx++)
        reg_write(baseaddr + idx, val[idx]);
}

void compare_multi_word(uint32_t baseaddr, uint32_t *val)
{
    int idx;
    // read inputs
    for( idx=0; idx < NWORDS_ECDSA256; idx++)
        check_reg_val(baseaddr + idx, val[idx]);
}

////////// Test functions //////////////////////////////

void test_read_registers(){

    check_reg_val(ADDR_NAME0, CORE_NAME0);
    check_reg_val(ADDR_NAME1, CORE_NAME1);
    check_reg_val(ADDR_VERSION, CORE_VERSION);
}

void test_rw_registers(){
    int ii, val;

    for (ii=0; ii < 32; ii++)
        {
            val = 1 << ii;
            reg_write(ADDR_DUMMY, val);
            check_reg_val(ADDR_DUMMY, val);
        }
}

void test_ecdsa_point_mul(const uint32_t *k, const uint32_t *qx, const uint32_t *qy){

    uint32_t status = 1;
    int niterations = 0;

    write_multi_word(ADDR_K, (uint32_t *) k);
    compare_multi_word(ADDR_K, (uint32_t *)k);

    status = reg_read(ADDR_STATUS);
    printf("STATUS: 0x%08x\n", status);

    reg_write(ADDR_CONTROL,0);
    reg_write(ADDR_CONTROL,3); // give one extra clock cycle
    reg_read(ADDR_CONTROL); // give one extra clock cycle
    
    status = reg_read(ADDR_STATUS);
    printf("STATUS: 0x%08x\n", status);

    while ((status < 3) && (niterations < ECDSA256_NCYCLES_TIMEOUT))
        {
        niterations++;
        status = reg_read(ADDR_STATUS);

        if ((niterations % 100000) == 0)
            printf("#ITERATIONS: %d, STATUS: 0x%08x\n", niterations, status);
        }

    printf("#ITERATIONS: %d, STATUS: 0x%08x\n", niterations, status);

    compare_multi_word(ADDR_QX,(uint32_t *)qx);
    compare_multi_word(ADDR_QY,(uint32_t *)qy);

    reg_write(ADDR_CONTROL,0);
}

/////////////// C tests top ///////////////////////////

void test_all()
{
    test_read_registers();
    test_rw_registers();
    test_ecdsa_point_mul(ECDSA_P256_D_NSA, ECDSA_P256_QX_NSA, ECDSA_P256_QY_NSA );
}
