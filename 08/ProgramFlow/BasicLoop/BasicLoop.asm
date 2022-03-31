// //// Processing None.vm
// File namespace changes to BasicLoop
// Translate command: push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: pop local 0         
@LCL
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
// Translate command: label LOOP_START
(LOOP_START)
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
// Translate command: pop local 0	        
@LCL
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
// Translate command: if-goto LOOP_START  
@SP
M=M-1
@SP
A=M
D=M
@LOOP_START
D;JNE
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
