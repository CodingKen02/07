// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/mult/Mult.tst

load StackBasicTest.hack,
output-file StackBasicTest.out,
compare-to StackBasicTest.cmp,
output-list RAM[0]%D2.6.2 RAM[13]%D2.6.2 RAM[14]%D2.6.2 RAM[15]%D2.6.2 ;

set RAM[0] 255,   // Set stack address
repeat 1000 {
  ticktock;
}
output;

