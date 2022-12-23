#include "dut.h"
#include "ecdsa256_hal.h"
#include "ecdsa256_test_vectors.h"
#include <iostream>

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

/////////////// C tests
DutTest *dut = new DutTest;

void test_all()
{
    dut->test_read_registers();
    dut->test_rw_registers();
    dut->test_ecdsa_point_mul(ECDSA_P256_D_NSA, ECDSA_P256_QX_NSA, ECDSA_P256_QY_NSA );
}
