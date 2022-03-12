
module dump;
    initial begin
        $dumpfile("dump.vcd");            
        $dumpvars(`DUMP_LEVEL,`DUMP_MODULE);
    end
endmodule