// //// Processing FibonacciSeries.vm
// File namespace changes to FibonacciSeries
// Translate command: push argument 1
@ARG
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// Translate command: pop pointer 1           
@R4
D=A
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R13
A=M
M=D
// Translate command: push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: pop that 0              
@THAT
D=M
@0
A=D+A
D=A
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R13
A=M
M=D
// Translate command: push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: pop that 1              
@THAT
D=M
@1
A=D+A
D=A
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R13
A=M
M=D
// Translate command: push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// Translate command: push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: sub
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M-D
@SP
M=M+1
// Translate command: pop argument 0          
@ARG
D=M
@0
A=D+A
D=A
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R13
A=M
M=D
// Translate command: label MAIN_LOOP_START
(MAIN_LOOP_START)
// Translate command: push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// Translate command: if-goto COMPUTE_ELEMENT 
@SP
M=M-1
@SP
A=M
D=M
@COMPUTE_ELEMENT
D;JNE
// Translate command: goto END_PROGRAM        
@END_PROGRAM
0;JMP
// Translate command: label COMPUTE_ELEMENT
(COMPUTE_ELEMENT)
// Translate command: push that 0
@THAT
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// Translate command: push that 1
@THAT
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// Translate command: add
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M+D
@SP
M=M+1
// Translate command: pop that 2              
@THAT
D=M
@2
A=D+A
D=A
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R13
A=M
M=D
// Translate command: push pointer 1
@R4
D=M
@SP
A=M
M=D
@SP
M=M+1
// Translate command: push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: add
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M+D
@SP
M=M+1
// Translate command: pop pointer 1           
@R4
D=A
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R13
A=M
M=D
// Translate command: push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// Translate command: push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: sub
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M-D
@SP
M=M+1
// Translate command: pop argument 0          
@ARG
D=M
@0
A=D+A
D=A
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R13
A=M
M=D
// Translate command: goto MAIN_LOOP_START
@MAIN_LOOP_START
0;JMP
// Translate command: label END_PROGRAM
(END_PROGRAM)
