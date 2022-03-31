// bootstrap code
@256
D=A
@SP
M=D
// push return address
@Sys.initRET0
D=A
@SP
A=M
M=D
@SP
M=M+1
// store LCL ARG THIS THAT
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// reposition LCL
@SP
D=M
@LCL
M=D
// reposition ARG (n=number of args)
@5
D=D-A
@ARG
M=D
// function call preparation done, ready to jump
@Sys.init
0;JMP
// create the returning point
(Sys.initRET0)
// //// Processing Sys.vm
// File namespace changes to Sys
// Translate command: function Sys.init 0
// define function Sys.init
(Sys.init)
// namespace changes to Sys.init
// Translate command: push constant 4000	
@4000	
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: pop pointer 0
@R3
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
// Translate command: push constant 5000
@5000
D=A
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
// Translate command: call Sys.main 0
// push return address
@Sys.mainRET1
D=A
@SP
A=M
M=D
@SP
M=M+1
// store LCL ARG THIS THAT
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// reposition LCL
@SP
D=M
@LCL
M=D
// reposition ARG (n=number of args)
@5
D=D-A
@ARG
M=D
// function call preparation done, ready to jump
@Sys.main
0;JMP
// create the returning point
(Sys.mainRET1)
// Translate command: pop temp 1
@R6
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
// Translate command: label LOOP
(Sys.init:LOOP)
// Translate command: goto LOOP
@Sys.init:LOOP
0;JMP
// Translate command: function Sys.main 5
// define function Sys.main
(Sys.main)
// namespace changes to Sys.main
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: push constant 4001
@4001
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: pop pointer 0
@R3
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
// Translate command: push constant 5001
@5001
D=A
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
// Translate command: push constant 200
@200
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: pop local 1
@LCL
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
// Translate command: push constant 40
@40
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: pop local 2
@LCL
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
// Translate command: push constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: pop local 3
@LCL
D=M
@3
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
// Translate command: push constant 123
@123
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: call Sys.add12 1
// push return address
@Sys.add12RET2
D=A
@SP
A=M
M=D
@SP
M=M+1
// store LCL ARG THIS THAT
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// reposition LCL
@SP
D=M
@LCL
M=D
// reposition ARG (n=number of args)
@6
D=D-A
@ARG
M=D
// function call preparation done, ready to jump
@Sys.add12
0;JMP
// create the returning point
(Sys.add12RET2)
// Translate command: pop temp 0
@R5
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
// Translate command: push local 0
@LCL
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// Translate command: push local 1
@LCL
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// Translate command: push local 2
@LCL
D=M
@2
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// Translate command: push local 3
@LCL
D=M
@3
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// Translate command: push local 4
@LCL
D=M
@4
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
// Translate command: return
@LCL
D=M
@R13
M=D
// RET = *(FRAME-5)
@R13
D=M
@5
D=D-A
A=D
D=M
@R14
M=D
// *ARG = pop
@SP
M=M-1
@SP
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@R13
D=M
@1
D=D-A
A=D
D=M
@THAT
M=D
@R13
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
@R13
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
@R13
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
// goto RET
@R14
A=M
0;JMP
// Translate command: function Sys.add12 0
// define function Sys.add12
(Sys.add12)
// namespace changes to Sys.add12
// Translate command: push constant 4002
@4002
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: pop pointer 0
@R3
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
// Translate command: push constant 5002
@5002
D=A
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
// Translate command: push constant 12
@12
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
// Translate command: return
@LCL
D=M
@R13
M=D
// RET = *(FRAME-5)
@R13
D=M
@5
D=D-A
A=D
D=M
@R14
M=D
// *ARG = pop
@SP
M=M-1
@SP
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@R13
D=M
@1
D=D-A
A=D
D=M
@THAT
M=D
@R13
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
@R13
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
@R13
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
// goto RET
@R14
A=M
0;JMP
