// Translate command: push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: eq
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@BOOL_START_0
D;JEQ
@SP
A=M
M=0
@BOOL_END_0
0;JMP
(BOOL_START_0)
@SP
A=M
M=-1
(BOOL_END_0)
@SP
M=M+1
// Translate command: push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: eq
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@BOOL_START_1
D;JEQ
@SP
A=M
M=0
@BOOL_END_1
0;JMP
(BOOL_START_1)
@SP
A=M
M=-1
(BOOL_END_1)
@SP
M=M+1
// Translate command: push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: eq
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@BOOL_START_2
D;JEQ
@SP
A=M
M=0
@BOOL_END_2
0;JMP
(BOOL_START_2)
@SP
A=M
M=-1
(BOOL_END_2)
@SP
M=M+1
// Translate command: push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: lt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@BOOL_START_3
D;JLT
@SP
A=M
M=0
@BOOL_END_3
0;JMP
(BOOL_START_3)
@SP
A=M
M=-1
(BOOL_END_3)
@SP
M=M+1
// Translate command: push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: lt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@BOOL_START_4
D;JLT
@SP
A=M
M=0
@BOOL_END_4
0;JMP
(BOOL_START_4)
@SP
A=M
M=-1
(BOOL_END_4)
@SP
M=M+1
// Translate command: push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: lt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@BOOL_START_5
D;JLT
@SP
A=M
M=0
@BOOL_END_5
0;JMP
(BOOL_START_5)
@SP
A=M
M=-1
(BOOL_END_5)
@SP
M=M+1
// Translate command: push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: gt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@BOOL_START_6
D;JGT
@SP
A=M
M=0
@BOOL_END_6
0;JMP
(BOOL_START_6)
@SP
A=M
M=-1
(BOOL_END_6)
@SP
M=M+1
// Translate command: push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: gt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@BOOL_START_7
D;JGT
@SP
A=M
M=0
@BOOL_END_7
0;JMP
(BOOL_START_7)
@SP
A=M
M=-1
(BOOL_END_7)
@SP
M=M+1
// Translate command: push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: gt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@BOOL_START_8
D;JGT
@SP
A=M
M=0
@BOOL_END_8
0;JMP
(BOOL_START_8)
@SP
A=M
M=-1
(BOOL_END_8)
@SP
M=M+1
// Translate command: push constant 57
@57
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: push constant 31
@31
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: push constant 53
@53
D=A
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
A=M
M=M+D
@SP
M=M+1
// Translate command: push constant 112
@112
D=A
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
A=M
M=M-D
@SP
M=M+1
// Translate command: neg
@SP
M=M-1
A=M
M=-M
@SP
M=M+1
// Translate command: and
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M&D
@SP
M=M+1
// Translate command: push constant 82
@82
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: or
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M|D
@SP
M=M+1
// Translate command: not
@SP
M=M-1
A=M
M=!M
@SP
M=M+1