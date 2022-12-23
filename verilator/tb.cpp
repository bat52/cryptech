#include <iostream>
#include "test.h"

int main(int argc, char** argv, char** env) {

    test_all();

    // delete dut;
    exit(EXIT_SUCCESS);
}