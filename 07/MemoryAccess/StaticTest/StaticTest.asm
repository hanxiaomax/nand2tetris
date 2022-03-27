// Translate command: push constant 111
@111
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: push constant 333
@333
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: push constant 888
@888
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: pop static 8
@StaticTest.8
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// Translate command: pop static 3
@StaticTest.3
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// Translate command: pop static 1
@StaticTest.1
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// Translate command: push static 3
@StaticTest.3
D=M
@SP
A=M
M=D
@SP
M=M+1
// Translate command: push static 1
@StaticTest.1
D=M
@SP
A=M
M=D
@SP
M=M+1
// Translate command: sub
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M-D
@SP
M=M+1
// Translate command: push static 8
@StaticTest.8
D=M
@SP
A=M
M=D
@SP
M=M+1
// Translate command: add
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M+D
@SP
M=M+1
