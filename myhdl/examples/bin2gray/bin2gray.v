// File: bin2gray.v
// Generated by MyHDL 0.11
// Date: Wed Dec 28 23:04:55 2022


`timescale 1ns/10ps

module bin2gray (
    B,
    G,
    EN
);
// Gray encoder.
// 
// B -- binary input 
// G -- Gray encoded output

input EN; 
input [3:0] B;
output [3:0] G;
wire [3:0] G;





assign G = EN ? ((B >>> 1) ^ B) : 0;

endmodule
