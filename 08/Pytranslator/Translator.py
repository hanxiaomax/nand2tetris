from enum import Enum
from CodeWriter import CodeWrite,arithmetic_type
import traceback

class CommandType(Enum):
    ARITHMETIC = 1,
    PUSH = 2,
    POP = 3,
    LABEL = 4,
    GOTO = 5,
    IF_GOTO = 6,
    FUNCTION = 7,
    RETURN = 8,
    CALL = 9

class Translator(object):
    def __init__(self,filename):
        self.input_filename = filename
        self.output_filename= filename.replace(".vm",".asm")
        self.in_file_handler = None
        self.out_file_handler = None
        self.commands = None
        self.index = 0
        self.asm_code = []
        self.cw = None

    def __str__(self):
        return "VM code translator"

    def __enter__(self):
        print("Open file ",self.input_filename)
        self.in_file_handler = open(self.input_filename,'r')
        self.out_file_handler = open(self.output_filename,'w')
        self.commands = self.in_file_handler.readlines()
        self.cw = CodeWrite(self.input_filename,self.out_file_handler)#the input filename used for static var
        self.cw.write_init() # call sys.init if exists
        return self

    def __exit__(self,exc_type,exc_val,exc_tb):
        if self.in_file_handler:
            print("Close input file: ",self.input_filename)
            self.in_file_handler.close()
        if self.out_file_handler:
            print("Close output file: ",self.output_filename)
            self.out_file_handler.close()
        if exc_val:
            print("exit:", exc_type, exc_val, exc_tb)
            print(traceback.print_tb(exc_tb))
        return True


    def has_more_cmd(self):
        """判断是否还有指令需要处理
        Returns:
            Boolean:
        """
        return len(self.commands)  != self.index
    
    def get_next_cmd(self):
        """取下一个指令，跳过注释
        Returns:
            string: 当前要处理的指令
        """
        while self.has_more_cmd:
            temp_cmd = self.trim_cmd(self.commands[self.index])
            self.index = self.index + 1 
            if temp_cmd!="":#if current line is empty after removing the comments, fetch next
                return temp_cmd

    def trim_cmd(self,cmd):
        cmd=cmd.strip()
        pos = cmd.find("//")
        return cmd[:pos] if pos >= 0 else cmd #delate comment in this line

    def run(self):
        print("Start translation...")
        while self.has_more_cmd():
            current = self.get_next_cmd() 
            current_tokens = self.tokenize(current)
            cmd_type = self.get_cmd_type(current_tokens[0])
            self.cw.write_comments("Translate command: {cmd}".format(cmd=current))
            if cmd_type == CommandType.POP or cmd_type == CommandType.PUSH:
                # self.cw.write_comments("Translate command: {cmd}".format(cmd=current))
                self.cw.write_push_pop(current_tokens[0],current_tokens[1],current_tokens[2])
            elif cmd_type == CommandType.ARITHMETIC:
                # self.cw.write_comments("Translate command: {cmd}".format(cmd=current))
                self.cw.write_arithmetic(current_tokens[0])
            elif cmd_type == CommandType.LABEL: # label (LABEL)
                self.cw.write_label(current_tokens[1])
            elif cmd_type == CommandType.GOTO: # goto (LABEL)
                self.cw.write_goto(current_tokens[1])
            elif cmd_type == CommandType.IF_GOTO:# if-goto (LABEL)
                self.cw.write_if(current_tokens[1])
            elif cmd_type == CommandType.FUNCTION:# function f k
                self.cw.write_function(current_tokens[1],int(current_tokens[2]))
            elif cmd_type == CommandType.RETURN:# return 
                self.cw.write_return()
            elif cmd_type == CommandType.CALL:# call f n
                self.cw.write_call(current_tokens[1],int(current_tokens[2]))
            else:
                raise NotImplementedError
            # print("{: <12}:  {: <30}".format(str(cmd_type).replace("CommandType.",""),current))
   
    def tokenize(self,cmd):
        tokens = cmd.lower().split(" ")
        map(lambda x:x.strip(),tokens)
        return tokens

    def get_cmd_type(self,cmd):
        if cmd == "pop":
            return CommandType.POP
        elif cmd == "push":
            return CommandType.PUSH
        elif cmd in arithmetic_type:
            return CommandType.ARITHMETIC
        elif cmd == "label":
            return CommandType.LABEL
        elif cmd == "goto":
            return CommandType.GOTO
        elif cmd == "if-goto":
            return CommandType.IF_GOTO
        elif cmd == "function":
            return CommandType.FUNCTION
        elif cmd == "return":
            return CommandType.RETURN
        elif cmd == "call":
            return CommandType.CALL
        else:
            raise NotImplementedError
