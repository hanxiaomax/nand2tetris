// Translate command: push constant 7
@7
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
