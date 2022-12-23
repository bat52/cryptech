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

#define ECDSA256_NCYCLES_TIMEOUT 1000000
