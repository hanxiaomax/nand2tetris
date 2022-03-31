import traceback

arithmetic_type = ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']
DEBUG = False
class CodeWriter(object):
    def __init__(self, output_file):
        self.asm_name = output_file 
        self.asm = None
        #用于static变量，但是不需要后缀，也不需要路径
        self.ns_file = None # namespace file
        self.ns_function = None # namespace function
        self.bool_label_index = 0
        self.call_label_index = 0
        self.base_registers = { 
            'local': 'LCL',
            'argument': 'ARG', 
            'this': 'THIS', 
            'that': 'THAT', 
            'pointer': 3, 
            'temp': 5, 
            'static': 16, 
        }
       
    def __enter__(self):
        print("Open file ",self.asm_name)
        self.asm = open(self.asm_name,'w')
        self.write_init() # call sys.init if exists
        return self

    def __exit__(self,exc_type,exc_val,exc_tb):
        print("CodeWriter exit, close ",self.asm_name)
        self.asm.close()
        if exc_val:
            print("exit:", exc_type, exc_val, exc_tb)
            print(traceback.print_tb(exc_tb))
        return True

    def set_current_vmfile(self,ns_file):
        self.ns_file = ns_file
        self.write_comments("//// Processing {}.vm".format(self.ns_file))


    def write_arithmetic(self,command):
        if command in ("not","neg"):#一元运算符
            self.decrement_sp_update()#SP-- 并指向当前栈顶元素
            self.write('M=-M') if command == 'neg' else self.write('M=!M')
        elif command in ("add","sub","and","or"):#二元运算符
            # 二元运算符需要操作栈上两个元素，必须先弹出一个，再指向另一个
            self.write_pop_from_stack() # 栈顶元素弹出到D
            self.decrement_sp_update()# SP-- 并指向当前栈顶元素
            # 此时D为栈顶弹出的元素，M为当前栈顶元素，两者可以直接参与运算
            if command == "add":
                self.write("M=M+D")
            elif command == "sub":
                self.write("M=M-D")
            elif command == 'and':
                self.write('M=M&D')
            elif command == 'or':
                self.write('M=M|D')
        elif command in ("eq", "gt", "lt"): #二元逻辑运算
            self.write_pop_from_stack() # 栈顶元素弹出到D
            self.decrement_sp_update()# SP-- 并指向当前栈顶元素
            self.write('D=M-D') # 将当前两个运算符比较大小存放到D
            #创建一个跳转指令，以便对D的值进行判断
            self.write("@BOOL_START_"+str(self.bool_label_index))
            if command == 'eq':
                self.write('D;JEQ') # if x == y, x - y == 0
            elif command == 'gt':
                self.write('D;JGT') # if x > y, x - y > 0
            elif command == 'lt':
                self.write('D;JLT') # if x < y, x - y < 0
            #Three of the commands (eq, gt, lt) return Boolean values. 
            # The VM represents 
            #  true  = -1 (minus one, 0xFFFF) 
            #  false = 0 (zero, 0x0000), respectively.
            
            # 没有执行跳转条件，表明判断条件不成立，栈顶赋值 False
            self.write("@SP")
            self.write("A=M")
            self.write('M=0') # False
            # 赋值结束，无条件跳转到结尾，防止走到else分支
            self.write('@BOOL_END_'+str(self.bool_label_index))
            self.write('0;JMP')
            # 执行跳转条件，表明判断条件成立，栈顶赋值 True
            self.write("(BOOL_START_{})".format(self.bool_label_index))
            self.write("@SP")
            self.write("A=M")
            self.write('M=-1') # True
            self.write("(BOOL_END_{})".format(self.bool_label_index))
            self.bool_label_index += 1
        
        self.increment_sp()#完成计算后，SP要指向栈顶空间，方便后面操作

    def write_push_pop(self,command,segment,index):
        # *SP = *addr, SP ++
        if command == "push": 
            self.write_address(segment,index)#已经选取了M=RAM[A]
            # constant这种特殊情况，需要存放的数据放在A中
            self.write("D=A") if segment == "constant" else self.write("D=M")
            self.write_push_to_stack()
        #SP-- , *addr = *SP
        elif command == "pop":
            if segment == "constant": raise #constant 不支持pop操作
            self.write_address(segment,index)#已经选取了M=RAM[A]
            #必须先将结果保存下来，否则执行pop操作时会覆盖寄存器
            #将地址存放到临时寄存器R13
            self.write('D=A') 
            self.write('@R13') 
            self.write('M=D')
            # 将当前栈顶元素弹出到D
            self.write_pop_from_stack()
            # 恢复addr，并将D存放到RAM[addr]
            self.write('@R13')
            self.write('A=M')
            self.write('M=D')

    def write_address(self,segment,index):
        """
        根据segment获取当前要操作的地址，分为如下几种情况
        1. constant：虚拟段，实际上是压栈，A寄存器做数据寄存器，直接赋值
        2. ("local","argument","this","that")：动态分布的段，需要访问基地址寄存器，并根据寄存器内地址，
        按指针操作确定基地址，然后加上段内偏移
        3. ("temp","pointer")：固定分布的段，访问基地址寄存器，寄存器内即存放基地址，直接加段内偏移
        4. static：需要基于文件名，创建一个@filename.i 标记
        """
        base_register = self.base_registers.get(segment)
        if segment == "constant":# constant is not real, just push it to stack
            self.write("@"+str(index)) #A=i
        elif segment in ("local","argument","this","that"): #dynamic segment (address = *base + i) 
            self.write("@" + base_register)  # select get base_register
            self.write("D=M") # get base address 
            self.write("@"+str(index))
            self.write("A=D+A") # base address + index
        elif segment in  ("temp","pointer"): #fixed segment, (address = base + i)
            self.write('@R'+ str(base_register + int(index))) #select Register Rx
        elif segment == "static": # global var use special label (@filename.i)
            self.write("@" + self.ns_file + '.' + str(index))
        else:
            print("[ERROR]Invalid segment: ",segment)
            raise NotImplementedError

    def decrement_sp(self):
        """
        将SP寄存器的值-1。注意，此时M并不是栈顶元素，因为A没有更新
        如果需要让M指向当前SP所指的元素，还必须执行
        @SP 
        A=M
        或直接调用 decrement_sp_update
        """
        self.write("@SP")
        self.write("M=M-1")

    def decrement_sp_update(self):
        """
        SP指针-1并更新地址寄存器A选择新的M，即栈顶元素
        """
        self.decrement_sp()
        self.write("@SP") #这个指令其实是多余的，因为A并没有改变，但是这么做能够防止出错
        self.write("A=M")

    def increment_sp(self):
        """
        将SP寄存器的值+1。注意，此时M并不是栈顶空位，因为A没有更新
        如果需要让M指向当前SP所指的内存位置，还必须执行
        @SP 
        A=M
        或直接调用 increment_sp_update
        """
        self.write("@SP")
        self.write("M=M+1")

    def increment_sp_update(self):
        """
        SP指针+1并更新地址寄存器A选择新的M，即栈顶元素
        """
        self.increment_sp()
        self.write("@SP") 
        self.write("A=M")
    
    def write_push_to_stack(self):
        """
        将D寄存器的值压入栈中，存放在栈顶位置，然后更新栈顶指针到下一个空闲位置
        """
        self.write("@SP") # get sp 
        self.write("A=M") # dereference SP
        self.write("M=D") # save D to top
        self.increment_sp() # decrement sp 

    def write_pop_from_stack(self):
        """
        SP指针-1然后将栈顶元素弹出存放到D
        """
        self.decrement_sp_update()
        self.write("D=M") #save top element to D

    def write(self,command):
        self.asm.write(command+"\r\n")

    def write_comments(self,comments):
        if DEBUG:
            self.write("// "+comments)

    def write_init(self):
        """
        初始化，需要在文件最开始调用
        SP=256
        call Sys.init
        """
        self.write_comments("bootstrap code")
        self.write("@256")
        self.write("D=A")
        self.write("@SP")
        self.write("M=D")
        self.write_call('Sys.init', 0)

    def write_label(self,label: str):
        """
        (LABEL)
        对于函数内的label，必须要以functionName:label的方式保证唯一性
        """
        if self.ns_function:
            self.write("({ns}:{label})".format(ns=self.ns_function,label=label))
        else:
            self.write("({label})".format(label=label))

    def write_goto(self,label: str):
        """
        无条件跳转
        """
        if self.ns_function:
            self.write('@{ns}:{label}'.format(ns=self.ns_function,label=label))
        else:
            self.write('@{label}'.format(label=label))
            
        self.write('0;JMP')

    def write_if(self,label: str):
        """
        有条件跳转，必须先弹出栈顶元素用于判断。
        该元素是前面的比较运算压入的结果
        """
        self.write_pop_from_stack()
        # self.write_label(label)
        self.write('@{label}'.format(label=label))
        self.write('D;JNE')#False = 0，因此必须使用JNE判断是否跳转
    
    def set_function_namespace(self,function_name):
        return 
        self.write_comments("namespace changes to {}".format(function_name))
        self.ns_function= function_name 

    def write_function(self,function_name:str,num_locals:int):
        """
        函数定义并初始化局部变量
        每个函数都需要创建一个 (functionName) 符号表示其入口
        """
        self.write_comments("define function {}".format(function_name))
        self.write('({function_name})'.format(function_name=function_name))
        self.set_function_namespace(function_name)
        # 在栈上创建 n 个局部变量
        for i in range(num_locals): 
            # push constant 0 
            # 等价于 self.write_push_pop("push","constant","0")
            self.write("@0")
            self.write('D=A')
            self.write_push_to_stack()
    
    def write_call(self,function_name: str,num_args:int):
        # return_label = self.create_retrun_lable(function_name)
        return_label = function_name + "RET" + str(self.call_label_index)
        self.call_label_index+=1
        # push return-address
        self.write_comments("push return address")
        self.write('@' + return_label)
        self.write('D=A')
        self.write_push_to_stack()
        
        self.write_comments("store LCL ARG THIS THAT")
        for address in ['@LCL', '@ARG', '@THIS', '@THAT']:
            self.write(address)
            self.write('D=M')
            self.write_push_to_stack()
        
        
        self.write_comments("reposition LCL")
        #reposition LCL
        self.write('@SP')
        self.write('D=M')
        self.write('@LCL')
        self.write('M=D')

        # ARG = SP-n-5
        self.write_comments("reposition ARG (n=number of args)")
        self.write('@' + str(num_args + 5))
        self.write('D=D-A')
        self.write('@ARG')
        self.write('M=D')
        
        self.write_comments("function call preparation done, ready to jump")
        self.write('@' + function_name)
        self.write('0;JMP')

        # (return_address)
        self.write_comments("create the returning point")

        self.write('({return_label})'.format(return_label=return_label))

    def write_return(self):
        
        # R13 for FRAME
        # R14 fro RETURN

        # FRAME = LCL
        self.write('@LCL')
        self.write('D=M')
        self.write('@R13')
        self.write('M=D')

        # RET = *(FRAME-5)
        self.write_comments("RET = *(FRAME-5)")
        self.write('@R13')
        self.write('D=M') # Save start of frame
        self.write('@5')
        self.write('D=D-A') # Adjust address
        self.write('A=D') # Prepare to load value at address
        self.write('D=M') # Store value
        self.write('@R14')
        self.write('M=D') # Save value

        # *ARG = pop
        self.write_comments("*ARG = pop")
        self.write_pop_from_stack()
        self.write('@ARG')
        self.write('A=M')
        self.write('M=D')

        # SP = ARG+1
        self.write('@ARG')
        self.write('D=M')
        self.write('@SP')
        self.write('M=D+1')

        # THAT = *(FRAME-1)
        # THIS = *(FRAME-2)
        # ARG = *(FRAME-3)
        # LCL = *(FRAME-4)
        offset = 1
        for address in ['@THAT', '@THIS', '@ARG', '@LCL']:
            self.write('@R13' )
            self.write('D=M') # Save start of frame
            self.write('@' + str(offset))
            self.write('D=D-A') # Adjust address
            self.write('A=D') # Prepare to load value at address
            self.write('D=M') # Store value
            self.write(address)
            self.write('M=D') # Save value
            offset += 1


        # goto RET
        self.write_comments("goto RET")
        self.write('@R14' )
        self.write('A=M')
        self.write('0;JMP')

        # self.set_function_namespace(None)