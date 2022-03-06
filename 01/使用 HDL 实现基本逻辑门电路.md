---
title: 使用 HDL 实现基本逻辑门电路
tag:
- topic 
--- 
---

🏷️ Status:: #herb   
📌 tags:: [[@nand]]
🔗 Parent::  `$= dv.current().file.inlinks`

# 使用 HDL 实现基本逻辑门电路
-----


- [[HDL语言]]

```toc

```


## 基本逻辑门

### NOT
按照公理1实现：`NOT(x) = x NAND x`
```c
CHIP Not {
    IN in;
    OUT out;

    PARTS:
    Nand(a=in,b=in,out=out);
}
```


### AND
首先使用最基础的与非门 NAND 来实现 AND

公理1：`NOT(x) = (x NAND x) `
公理2：`(x AND y) = NOT (x NAND y) `
// replace x with (x NAND y)
实现：(x AND y) = NOT (x NAND y) = ((x NAND y) NAND (x NAND y))
即 x AND y 可以使用三个 NAND 门实现

```c
/**
 * And gate: 
 * out = 1 if (a == 1 and b == 1)
 *       0 otherwise
*/
CHIP And {
    IN a, b;
    OUT out;

    PARTS:
    // Put your code here:
    Nand(a=a,b=b,out=o1); //(x NAND y)
    Nand(a=a,b=b,out=o2);//(x NAND y)
    Nand(a=o1,b=o2,out=out); //  (x AND y) = NOT (x NAND y) = ((x NAND y) NAND (x NAND y))
}

```


### OR
根据 `x OR y = NOT(NOT (x) AND NOT(y))`
使用NOT和AND实现
```c
CHIP Or {
    IN a, b;
    OUT out;

    PARTS:
    // Put your code here:
    Not(in=a,out=nota);
    Not(in=b,out=notb);
    And(a=nota,b=notb,out=notaandnotb);
    Not(in=notaandnotb,out=out); 
}
```

### XOR
- `Xor = x AND NOT(y) OR NOT(x) AND y `可以直接使用AND、NOT和OR实现。
- [4个NAND的实现方法](https://cs.stackexchange.com/questions/43342/how-to-construct-xor-gate-using-only-4-nand-gate)

```c
CHIP Xor {
    IN a, b;
    OUT out;

    PARTS:
    Not(in=a,out=nota);
	Not(in=b,out=notb);
	And(a=a,b=notb,out=anotb);
	And(a=b,b=nota,out=bnota);
	Or(a=anotb,b=bnota,out=out);
}
```

```ad-note
**异或**也叫半加运算，其运算法则相当于不带进位的二进制加法：二进制下用1表示真，0表示假，则**异或**的运算法则为：0⊕0=0，1⊕0=1，0⊕1=1，1⊕1=0（同为0，**异**为1），这些法则与加法是相同的，只是不带进位，所以**异或**常被认作不进位加法。

异或可以通过四个NAND实现，当然也有其他实现方法，求最佳的方法是上一个复杂问题。
```

### Mux 单路输出 复用
当sel=1时，输出b，否则输出a
`Mux(a,b) = Or( (B and sel) ,(A and Not(sel)))`
```c
CHIP Mux {
    IN a, b, sel;
    OUT out;

    PARTS:
    And(a=b,b=sel,out=bandsel);
    Not(in=sel,out=notsel);
    And(a=a,b=notsel,out=aandnotsel);
    Or(a=bandsel,b=aandnotsel,out=out);
}
```

### DMux 多路输出复用
如果sel=1，则将a输出，否则把b输出
`out: a = And(in, Not(sel)), b = And(in, sel)`

```c
CHIP DMux {
    IN in, sel;
    OUT a, b;

    PARTS:
    // Put your code here:
    Not(in=sel,out=notsel);
    And(a=in,b=notsel,out=a);
    And(a=in,b=sel,out=b);
}

```

## 16位版本逻辑门
索引是从右向左的
### Not16
### And16
### Or16
### Mux16
只需要把1bit版本按照bus位执行16次即可。
```c
CHIP Not16 {
    IN in[16];
    OUT out[16];

    PARTS:
    Not(in = in[0], out = out[0]);
    Not(in = in[1], out = out[1]);
    Not(in = in[2], out = out[2]);
    Not(in = in[3], out = out[3]);
    Not(in = in[4], out = out[4]);
    Not(in = in[5], out = out[5]);
    Not(in = in[6], out = out[6]);
    Not(in = in[7], out = out[7]);
    Not(in = in[8], out = out[8]);
    Not(in = in[9], out = out[9]);
    Not(in = in[10], out = out[10]);
    Not(in = in[11], out = out[11]);
    Not(in = in[12], out = out[12]);
    Not(in = in[13], out = out[13]);
    Not(in = in[14], out = out[14]);
    Not(in = in[15], out = out[15]);
}
```

## 多路复用变种
### Or8Way 8路输入或门（8位按位取或）
```c
CHIP Or8Way {
    IN in[8];
    OUT out;

    PARTS:
    // Put your code here:
    Or(a = in[0], b = in[1], out = o1);
    Or(a = o1, b = in[2], out = o2);
    Or(a = o2, b = in[3], out = o3);
    Or(a = o3, b = in[4], out = o4);
    Or(a = o4, b = in[5], out = o5);
    Or(a = o5, b = in[6], out = o6);
    Or(a = o6, b = in[7], out = out);
}
```
### Mux4Way16 16位版本多路复用，4路输入
`out = a if sel == 00 b if sel == 01 c if sel == 10 d if sel == 11`
采用二分法的方式，选择两次即可。sel的高位确定ab还是cd。先根据低位确定a还是b，或者c还是d。然后通过高位选出真正的值。

```c
CHIP Mux4Way16 {
    IN a[16], b[16], c[16], d[16], sel[2];
    OUT out[16];

    PARTS:
    // Put your code here:
    Mux16(a = a, b = b, sel = sel[0], out = amuxb);
    Mux16(a = c, b = d, sel = sel[0], out = cmuxd);

    Mux16(a = o1, b = o2, sel = sel[1], out = out);
}
```
### Mux8Way16 16位版本多路复用，8路输入
可以通过两个Mux4Way16先在4路中选一个输出，然后通过Mux16在8路中确定是第一个4路还是第二个4路。

```c
CHIP Mux8Way16 {
    IN a[16], b[16], c[16], d[16],
       e[16], f[16], g[16], h[16],
       sel[3];
    OUT out[16];

    PARTS:
    Mux4Way16(a = a, b = b, c = c, d = d, sel = sel[0..1], out = o1);
    Mux4Way16(a = e, b = f, c = g, d = h, sel = sel[0..1], out = o2);

    Mux16(a = o1, b = o2, sel = sel[2], out = out);
}
```


### DMux4Way 4路输出中选择1路进行输出
根据4路输入，选择两路输出。使用3个DMux，先从4路选择1路，再从一个4路中选择1路，然后从两路中选择1路
![](https://nand2tetris-hdl.github.io/img/dmux4.png)
```c
CHIP DMux4Way {
    IN in, sel[2];
    OUT a, b, c, d;

    PARTS:
    // Put your code here:
    DMux(in = in, sel = sel[1], a = o1, b = o2);

    DMux(in = o1, sel = sel[0], a = a, b = b);
    DMux(in = o2, sel = sel[0], a = c, b = d);
}
```

### DMux8Way 8路输出中选择1路进行输出
先用一个DMux，将8路分成两个4路，然后用两个DMux4Way分别从两个4路中进行选择。
![](https://nand2tetris-hdl.github.io/img/dmux8.png)
```c
CHIP DMux8Way {
    IN in, sel[3];
    OUT a, b, c, d, e, f, g, h;

    PARTS:
    DMux(in = in, sel = sel[2], a = o1, b = o2);
    DMux4Way(in = o1, sel = sel[0..1], a = a, b = b, c = c, d = d);
    DMux4Way(in = o2, sel = sel[0..1], a = e, b = f, c = g, d = h);
}
```

## 寄存器
### Bit
![](https://nand2tetris-hdl.github.io/img/bit.png)
### Register

### PC
![](https://nand2tetris-hdl.github.io/img/pc.png)

## 内存
### RAM8
![](https://nand2tetris-hdl.github.io/img/ram8.png)

### RAM64


### RAM512
### RAM4K
### RAM16K
![](https://nand2tetris-hdl.github.io/img/ram16k.png)
-----

## 实现参考
- https://en.wikipedia.org/wiki/NAND_logic#XOR
- [# HDL API & Gate Design Reference](https://nand2tetris-hdl.github.io/)

