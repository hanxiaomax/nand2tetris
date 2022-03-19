// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
// 思路 :
// 1. 死循环检测是否有按键
// 2.根据按键情况跳转到 FILL 或者 CLEAR 并在内部设置R1的颜色为黑(-1)或者白(0)
// 3.跳转到填充函数处理填充，R1作为参数，存放了当前要填充的颜色
// 4. R0存放当前填充的地址，根据R0作指针取像素值并填充
// 5. 比较下一个地址和KBD是否相同，如果小于说明没填完继续填，否则跳转到最开始，复位地址
(START)
    //R0存放显示屏内存起始的地址
        //给一个地址赋值必须经过以下步骤
        //首先赋值给A，然后把A作为数据寄存器赋值给D（作为中间变量）
        //然后再赋值给A，选择目的地址，将A作为地址寄存器，自动选择M=RAM[A]
        //然后将D赋值给M完成赋值
    @SCREEN//16348
    D=A
    @R0 
    M=D    

    // // R1 存放当前要填充的颜色，是FUNC_CHANGE_COLOR的参数
    // @0//默认填充白色
    // D = A
    // @R1 //存放在R0中，应该使用Rx增强可读性
    // M = D

// 创建一个死循环，检查键盘输入
(CHECK_KBD_LOOP)
    @KBD// 加载键盘内存的数据
    D = M
    
    @FILL// if > 0 跳转到屏幕填充
    D;JGT

    @CLEAN
    D;JEQ// 数据为空，跳转到屏幕清除

(FILL)
    @R1 //获取R1的值并修改为要填充的颜色
    M = -1
    @FUNC_CHANGE_COLOR
    0;JMP

(CLEAN)
    @R1 //获取R1的值并修改为要填充的颜色
    M = 0
    @FUNC_CHANGE_COLOR
    0;JMP

(FUNC_CHANGE_COLOR)
        //取当前待填充颜色
        @R1 
        D = M 
        
        @R0  // R0 取出当前屏幕像素的地址
        A = M //取地址 ，根据地址指针，确定新的数据位置，但是@D这样的语法不行，必须赋值给A
        M = D  // 填充
        
        //判断屏幕是否已经填充完毕，即判断当前址是否等于KBD
        //注意当前地址不能用A表示，因为@KBD时会给A重新赋值为KBD
        @R0
        D=M+1   //从R0取出当前像素地址,+1计算下一步要填充的地址
        @KBD  //24576
        D = D - A  // 计算当前地址和KBD地址的差，这里会是一个小于等于0的值

        @R0 
        M=M+1   //地址递增
        A = M  // 新地址取值

        //如果当前地址和KBD的差小于0。说明还没有填充完
        @FUNC_CHANGE_COLOR
        D;JLT 

        //如果填充完，则返回监听
        @START
        0;JMP