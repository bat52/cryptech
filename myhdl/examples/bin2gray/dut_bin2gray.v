module dut_bin2gray;

   reg [`width-1:0] B;
   reg EN;
   wire [`width-1:0] G;

   initial begin
      $from_myhdl(B,EN);
      $to_myhdl(G);

      `ifdef DUMP_EN
         $dumpfile("dump.vcd");            
         $dumpvars(`DUMP_LEVEL,`DUMP_MODULE);         
      `endif
         
   end

   bin2gray dut (.B(B), .G(G), .EN(EN));
   // defparam dut.width = `width;

endmodule