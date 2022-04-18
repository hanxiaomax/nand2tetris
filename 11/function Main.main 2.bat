function Main.main 2
push constant 8001
push constant 16
push constant 1
neg
call Main.fillMemory 3
pop temp 0
push constant 8000
call Memory.peek 1
pop local 1
push local 1
call Main.convert 1
pop temp 0
push constant 0
return
function Main.convert 3
push constant 0
not
pop local 2
label WHILE0
push local 2
not
if-goto WHILE_END0
push local 1
push constant 1
add
pop local 1
push local 0
call Main.nextMask 1
pop local 0
push constant 9000
push local 1
add
push local 0
call Memory.poke 2
pop temp 0
push local 1
push constant 16
gt
not
if-goto IF_TRUE0
goto IF_FALSE0
label IF_TRUE0
push argument 0
push local 0
and
push constant 0
eq
not
if-goto IF_TRUE1
goto IF_FALSE1
label IF_TRUE1
push constant 8000
push local 1
add
push constant 1
call Memory.poke 2
pop temp 0
goto IF_END1
label IF_FALSE1
push constant 8000
push local 1
add
push constant 0
call Memory.poke 2
pop temp 0
label IF_END1
goto IF_END0
label IF_FALSE0
push constant 0
pop local 2
label IF_END0
goto WHILE0
label WHILE_END0
push constant 0
return
function Main.nextMask 0
push argument 0
push constant 0
eq
if-goto IF_TRUE2
goto IF_FALSE2
label IF_TRUE2
push constant 1
return
goto IF_END2
label IF_FALSE2
push argument 0
push constant 2
call Math.multiply 2
return
label IF_END2
function Main.fillMemory 0
label WHILE1
push argument 1
push constant 0
gt
not
if-goto WHILE_END1
push argument 0
push argument 2
call Memory.poke 2
pop temp 0
push argument 1
push constant 1
sub
pop argument 1
push argument 0
push constant 1
add
pop argument 0
goto WHILE1
label WHILE_END1
push constant 0
return