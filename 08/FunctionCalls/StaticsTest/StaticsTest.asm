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
// //// Processing Class1.vm
// File namespace changes to Class1
// Translate command: function Class1.set 0
// define function Class1.set
(Class1.set)
// namespace changes to Class1.set
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
// Translate command: pop static 0
@Class1.0
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
// Translate command: pop static 1
@Class1.1
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
// Translate command: function Class1.get 0
// define function Class1.get
(Class1.get)
// namespace changes to Class1.get
// Translate command: push static 0
@Class1.0
D=M
@SP
A=M
M=D
@SP
M=M+1
// Translate command: push static 1
@Class1.1
D=M
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
// //// Processing Sys.vm
// File namespace changes to Sys
// Translate command: function Sys.init 0
// define function Sys.init
(Sys.init)
// namespace changes to Sys.init
// Translate command: push constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: push constant 8
@8
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: call Class1.set 2
// push return address
@Class1.setRET1
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
@7
D=D-A
@ARG
M=D
// function call preparation done, ready to jump
@Class1.set
0;JMP
// create the returning point
(Class1.setRET1)
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
// Translate command: push constant 23
@23
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: push constant 15
@15
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: call Class2.set 2
// push return address
@Class2.setRET2
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
@7
D=D-A
@ARG
M=D
// function call preparation done, ready to jump
@Class2.set
0;JMP
// create the returning point
(Class2.setRET2)
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
// Translate command: call Class1.get 0
// push return address
@Class1.getRET3
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
@Class1.get
0;JMP
// create the returning point
(Class1.getRET3)
// Translate command: call Class2.get 0
// push return address
@Class2.getRET4
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
@Class2.get
0;JMP
// create the returning point
(Class2.getRET4)
// Translate command: label WHILE
(Sys.init:WHILE)
// Translate command: goto WHILE
@Sys.init:WHILE
0;JMP
// //// Processing Class2.vm
// File namespace changes to Class2
// Translate command: function Class2.set 0
// define function Class2.set
(Class2.set)
// namespace changes to Class2.set
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
// Translate command: pop static 0
@Class2.0
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
// Translate command: pop static 1
@Class2.1
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
// Translate command: function Class2.get 0
// define function Class2.get
(Class2.get)
// namespace changes to Class2.get
// Translate command: push static 0
@Class2.0
D=M
@SP
A=M
M=D
@SP
M=M+1
// Translate command: push static 1
@Class2.1
D=M
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
