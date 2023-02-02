// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/mult/Mult.tst

load OperatorTest.hack,
output-file OperatorTest.out,
compare-to OperatorTest.cmp,
output-list RAM[0]%D2.6.2 RAM[16]%D2.6.2 RAM[17]%D2.6.2 RAM[18]%D2.6.2 RAM[19]%D2.6.2 RAM[20]%D2.6.2 RAM[21]%D2.6.2 RAM[22]%D2.6.2 RAM[23]%D2.6.2 RAM[24]%D2.6.2 ;

set RAM[0] 255,   // Set test arguments
repeat 400 {
  ticktock;
}
output;

