from enum import Enum
from CodeWriter import arithmetic_type
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
    def __init__(self,vmfile):
        self.vmfile = vmfile
        self.vmfilehandler = open(self.vmfile,"r")
        self.commands = None
        self.index = 0
        self.cw = None

    def __str__(self):
        return "VM code translator"

    def set_codewriter(self,codewriter):
        self.cw = codewriter
    
    def close(self):
        self.vmfilehandler.close()

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


    def translate(self):
        print("Start translation...",self.vmfile)
        self.commands = self.vmfilehandler.readlines()
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
        # 不能直接转成小写，对于参数要保持其大小写，命令可以在判断的时候转
        tokens = cmd.split(" ")
        map(lambda x:x.strip(),tokens)
        return tokens

    def get_cmd_type(self,cmd):
        cmd = cmd.lower()
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
