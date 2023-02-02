$include Stack.h

//-----------------------------------------------------------------------------
// Arithmetic Operators
//-----------------------------------------------------------------------------

//-----------------------------------------------------------------------------
// Pop two items off of the stack (x and y), add them and push the result (x+y) on the stack
$def add
// pop ptr (store in R15)
$popAD
@R15
M=D
// pop value (store in D reg)
$popAD
// get value from R15
@R15
// add x and y
D=D+M
// pushes x+y
$pushD
$end

//-----------------------------------------------------------------------------
// Pop two items off of the stack (x and y), subtract them and push result (x-y) onto stack
$def sub
// pop ptr (store in R15)
$popAD
@R15
M=D
// pop value (store in D reg)
$popAD
// get value from R15
@R15
// subtract x and y
D=D-M
// pushes X - Y
$pushD
$end

//-----------------------------------------------------------------------------
// Pop one item off of the stack (x), negate it and push result (-x) onto stack
$def neg
// pop value (store in D reg)
$popAD
// negate x
D=-D
// pushes -x
$pushD
$end

//-----------------------------------------------------------------------------
// Comparison Operators
//-----------------------------------------------------------------------------

//-----------------------------------------------------------------------------
// Pop two items off of the stack (x and y), if x==y push -1 ; else push 0
$def eq
// subtracts the two values and pops the result
$sub
$popAD
// jump to TRUE if the result is 0
@TRUE
D;JEQ
// jump to FALSE otherwise
@FALSE
0;JMP
// D=-1 if x==y else D=0
(TRUE)
D=-1
// jump to end
@EXIT
0;JMP
// else
(FALSE)
D=0
(EXIT)
// pushes result onto stack
$pushD
$end

//-----------------------------------------------------------------------------
// Pop two items off of the stack (x and y), if y<x push -1 ; else push 0
$def lt
// subtracts the two values and pops the result
$sub
$popAD
// jump to TRUE if the result is < 0
@TRUE
D;JLT
// jump to FALSE otherwise
@FALSE
0;JMP
// D=-1 if x-y<0 else D=0
(TRUE)
D=-1
// jump to end
@EXIT
0;JMP
// else
(FALSE)
D=0
(EXIT)
// pushes result onto stack
$pushD
$end

//-----------------------------------------------------------------------------
// Pop two items off of the stack (x and y), if y>x push -1 ; else push 0
$def gt
// subtracts the two values and pops the result
$sub
$popAD
// jump to TRUE if the result is > 0
@TRUE
D;JGT
// jump to FALSE otherwise
@FALSE
0;JMP
// D=-1 if x-y>0 else D=0
(TRUE)
D=-1
// jump to end
@EXIT
0;JMP
// else
(FALSE)
D=0
(EXIT)
// pushes result onto stack
$pushD
$end

//-----------------------------------------------------------------------------
// Boolean Operators
//-----------------------------------------------------------------------------

//-----------------------------------------------------------------------------
// Pop two items off of the stack (x and y), bitwise-and them and push result (x&y) onto stack
$def and
// pop ptr (store in R15)
$popAD
@R15
M=D
// pop value (store in D reg)
$popAD
// get value from R15
@R15
// and x and y
D=D&M
// pushes x&y
$pushD
$end

//-----------------------------------------------------------------------------
// Pop two items off of the stack (x and y), bitwise-or them and push result (x|y) onto stack
$def or
// pop ptr (store in R15)
$popAD
@R15
M=D
// pop value (store in D reg)
$popAD
// get value from R15
@R15
// or x and y
D=D|M
// pushes x|y
$pushD
$end

//-----------------------------------------------------------------------------
// Pop one item off of the stack (x), bitwise-not it and push result (!x) onto stack
$def not
// pop value (store in D reg)
$popAD
// not x
D=!D
// pushes !x
$pushD
$end

//-----------------------------------------------------------------------------
// Go into infinite loop to halt the program
$def halt
@HALT
(HALT)
0;JMP
$end

// SP - R0
// LCL - R1
// ARG - R2
// THIS - R3
// THAT - R4
// R5 - R15 are random/default; then you will have more default parts including Data, Memory & Address Registers, etc.

// Every comment given above was understandable, especially when you follow the submitted video and spreadsheet. This header file is needed for Procedure.h which also requires the Stack.h file.