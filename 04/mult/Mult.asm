// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.
// 
    @R2
    M = 0

(LOOP)
//将R0循环R1次相加
    @R1
    D = M // 判断剩余循环次数是否为0
    @END
    D;JEQ//结束循环

    @R0 
    D = M //取 R0的值

    @R2
    M = M + D//进行一次加R0到R2

    @R1 
    M = M - 1  // R1--

    @LOOP
    0;JMP

(END)
    @END
    0;JMP