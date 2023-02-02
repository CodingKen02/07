// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/mult/Mult.tst

load ProcedureBasicTest.hack,
output-file ProcedureBasicTest.out,
compare-to ProcedureBasicTest.cmp,
output-list RAM[0]%D2.6.2 RAM[15]%D2.6.2 ;

set RAM[0] 28,   // Set stack address
repeat 1000 {
  ticktock;
}
output;

