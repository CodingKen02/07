load ProcedureTest.hack,
output-file ProcedureTest.out,
compare-to ProcedureTest.cmp,
output-list RAM[0]%D2.6.2 RAM[1]%D2.6.2 RAM[2]%D2.6.2 RAM[3]%D2.6.2 RAM[4]%D2.6.2 RAM[16]%D2.6.2 RAM[17]%D2.6.2 RAM[18]%D2.6.2 RAM[19]%D2.6.2 RAM[20]%D2.6.2 RAM[21]%D2.6.2 RAM[22]%D2.6.2 RAM[23]%D2.6.2 RAM[24]%D2.6.2 RAM[256]%D2.6.2 ;

set RAM[0] 255,   // Set stack address
set RAM[1]  -1,
set RAM[2]  -2,
set RAM[3]  -3,
set RAM[4]  -4,
set RAM[256] -1,
repeat 400000 {
  ticktock;
}
output;

