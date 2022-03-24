from Code import Code
from enum import Enum
from SymbolTable import SymbolTable
import re 
import sys
#### 注意事项
# 1. 第一遍处理只找(LABEL)，并且创建<label,pc>
# 2. 第二遍处理时，@xxx中的xxx可能是数，也可能是变量名
# 如果是变量名还要创建<var,free_ram_address>并完成转换

class CommandType(Enum):
    A_COMMAND =1
    C_COMMAND =2
    L_COMMAND =3

class Parser(object):
    def __init__(self,filename):
        self.filename = filename
        # self.current_cmd = None
        self.commands = None
        self.a_cmd_pattern = re.compile(r"^@(?P<address>\w.*)")
        self.l_cmd_pattern = re.compile(r"\((?P<label>.+)\)") 
        self.c_cmd_pattern = re.compile(r"(?P<dest>.*)=(?P<comp>.*)|(?P<comp2>.*)(?P<jump>;.*)") 
        self.c_cmd_match = None
        self.l_cmd_match = None
        self.a_cmd_match = None
        self.binary = [] #存放二进制机器码
        self.index = 0 #当前遍历的汇编文件的行号
        self.symbol_table = SymbolTable() # 符号表
        self.free_ram_address = 16 #第一个RAM空闲地址
        # pogram counter, basic the line of binary code. and it is the pos Lable should jump
        # only increment when Instruction is A or C
        self.pc = -1  #指令计数器，相当于指令在ROM中的位置，也是机器码文件的行号
        
    def build_symbol_table(self):
        """构建符号表
        搜索(LABEL)，并且创建<label,pc>
        pc 为指令计数器，表明当前符号在ROM中对应的指令位置
        注意不是RAM中的地址
        """
        # deal with symbols and addresses 
        with open(self.filename,"r") as f:
            self.commands = f.readlines()
            while self.has_more_cmd():
                current = self.advance() # fetch next valid command
                if(self.command_type(current)==CommandType.L_COMMAND):
                    # (LABLE) not considered as an Instruction, so pc will not increase 
                    # howerver,because when jump to the label, we want to excute its next Instruction
                    # so we store pc + 1 with the lable.
                    # And next Instruction's should start from pc instead of pc+1
                    self.symbol_table.addEntry(self.symbol(),self.pc+1)
                else:
                    self.pc +=1
            print(self.symbol_table.table)
            self.index = 0 #reset the index to the begin of code


    def parse(self):
        """第二遍遍历，将指令转换为二进制机器码
        """
        self.build_symbol_table() #第一次遍历构建符号表
        while self.has_more_cmd():
            current = self.advance() 
            print(current)
            if(self.command_type(current)==CommandType.A_COMMAND):
                value = self.symbol()
                if value.isdecimal(): # if the value is int then it is a A instruction
                    aa = Code.address(value) #covert int to bin directly 
                else:
                    if(self.symbol_table.contains(value)):
                        val = self.symbol_table.get_address(value)
                        aa = Code.address(val)
                    else:
                        # 第一次遇到@xxx中xxx为字符串的时候，创建变量，在RAM上为其分配一个地址
                        self.symbol_table.addEntry(value,self.free_ram_address)
                        aa = Code.address(self.free_ram_address)#完成转换并将RAM空闲地址+1
                        self.free_ram_address+=1
                self.binary.append(aa)
            elif(self.command_type(current)==CommandType.C_COMMAND):
                dd = Code.dest(self.dest())
                cc = Code.comp(self.comp())
                jj = Code.jump(self.jump())
                self.binary.append("111"+cc+dd+jj)
            else:
                #second pass ignore labels
                pass 
    
    def has_more_cmd(self):
        """判断是否还有指令需要处理
        Returns:
            Boolean:
        """
        return len(self.commands)  != self.index

    
    def trim_cmd(self,cmd):
        """清理指令，去除空格，删除行内注释
        Args:
            cmd (_type_): 需要清理的指令
        Returns:
            string: 不包含注释和空格的干净指令，用于正则匹配
        """
        cmd=cmd.strip().replace(" ","")
        pos = cmd.find("//")
        return cmd[:pos] if pos >= 0 else cmd #delate comment in this line
            
        
    def advance(self):
        """取下一个指令，跳过注释
        Returns:
            string: 当前要处理的指令
        """
        while self.has_more_cmd:
            temp_cmd = self.trim_cmd(self.commands[self.index])
            self.index = self.index + 1 
            if temp_cmd!="":#if current line is empty after removing the comments, fetch next
                return temp_cmd

    
    def command_type(self,current):
        """判断当前指令的类型
        通过正则匹配判断当前指令类型，同时将匹配结果存储下来
        Args:
            current (string): 当前指令
        Returns:
            CommandType: 指令类型
        """
        self.a_cmd_match = self.a_cmd_pattern.match(current)
        self.c_cmd_match = self.c_cmd_pattern.match(current)
        self.l_cmd_match = self.l_cmd_pattern.match(current)
        if self.a_cmd_match:
            return CommandType.A_COMMAND
        elif self.l_cmd_match:
            return CommandType.L_COMMAND
        elif self.c_cmd_match:
            return CommandType.C_COMMAND
        else:
            raise

    def symbol(self):
        """返回符号，可以是一个L伪指令中的符号
        也可以是A指令中的变量名，取决于指令类型
        Returns:
            string: 符号token
        """
        if self.l_cmd_match:
            return self.l_cmd_match.group("label")
        elif self.a_cmd_match:
            return self.a_cmd_match.group("address")
        else:
            raise
    
    def dest(self):
        if self.c_cmd_match:
            return self.c_cmd_match.group("dest")
        else:
            raise 
    
    def comp(self):
        if self.c_cmd_match:
            _comp = self.c_cmd_match.group("comp") 
            return _comp if _comp else self.c_cmd_match.group("comp2") 
        else:
            raise  

    def jump(self):
        if self.c_cmd_match:
            return self.c_cmd_match.group("jump")
        else:
            raise  


def compare_result(output):
    print("------- TEST -------")
    count = 0
    errors = 0
    groundtrue = output.replace("-my.hack",".hack")
    with open(output,'r') as o , open(groundtrue,'r') as t : 
        lines1 = o.readlines()
        lines2 = t.readlines()
        if len(lines1) != len(lines2):
            print("[ERROR]Lines of Code is not the same")
        else:
            for l1,l2 in zip(lines1,lines2):
                count +=1
                if l1 != l2:
                    errors+=1
                    print("at Line {} :\n {} \n {}".format(count,l1,l2),end="")
        print("Total errors: {}".format(errors))
        print("----- Finished -----")


if __name__ == "__main__":
    filename = sys.argv[1]
    binary = filename.replace(".asm","-my.hack")
    parser = Parser(filename)
    parser.parse()
    with open(binary,'w') as target:
        print("Total instructions: ",parser.pc+1)#pc is the index, so the number should + 1
        print("Output LOC: ",len(parser.binary))
        target.writelines("\n".join(parser.binary))
        target.write("\n")
    
    compare_result(binary)