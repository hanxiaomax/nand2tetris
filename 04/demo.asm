// Add up two numbers
// RAM[2] = RAM[0] + RAM[1]
// usage:put the values that you wish to add in RAM[0] and RAM[1]
//
@0 //获取地址0，此时M=RAM[0]
D=M//将RAM[0]中的值读取到D

@1//获取地址1，此时M=RAM[1]
D=D+M//将RAM[1]中的值与D中的值相加并读取到D

@2//获取地址2，此时M=RAM[2]
M=D//在RAM[2]中存放运算结果
@6
0;JMP