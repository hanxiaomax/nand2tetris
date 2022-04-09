import re 
from collections import deque


class JackTokenizer(object):
    def __init__(self,filename):
        self.filename = filename
        self.code_lines = self.read_code()
        self.raw_tokens = self.get_raw_tokens()
        self.print_code()
        self.print_raw_tokens()
        self.lexical_element = LexicalElement()
        self.token_type = None
        self.current_token = None
    
    def print_code(self):
        print("-"*20)
        for codeline in self.code_lines:
            print(codeline)
        print("-"*20)

    def print_raw_tokens(self):
        print("-"*20)
        for token in self.raw_tokens:
            print(token)
        print("-"*20)

    def read_code(self):
        """
        1. 忽略空行
        2. 忽略注释，包括多行注释，单行注释和行内注释
        """
        in_comment = False
        jack_codes = []
        with open(self.filename,"r") as f:
            for line in  f.readlines():
                line = line.strip().split("//")[0]# ignore inline comments 
                if not in_comment:
                    # single line comment
                    if line.startswith("//") or (line.startswith("/*") and line.endswith("*/")):
                        # print("#single line comment")
                        pass
                    # multi line comment start
                    elif line.startswith("/*"):
                        in_comment = True
                        # print("#multi line comment- IN")
                    elif line !='':
                        jack_codes.append(line) 
                        # print("#Add codeline")
                # multi line comment end
                elif line.startswith("*/") or line.endswith("*/"):
                        in_comment = False
                        # print("#multi line comment- OUT")
                else:#multi line comments content
                    pass

        # print(jack_codes)
        return jack_codes
    
    def get_raw_tokens(self):
        tokens = []
        for code_line in self.code_lines:
            tokens.extend(code_line.split())
        return deque(tokens)

    def has_more_tokens(self):
        return self.raw_tokens

    def advance(self):
        """
        处理raw_tokens，根据实际情况，
        进行再次切分或重组，返回的结果是一个合法的token
        """
        raw_token = self.raw_tokens.popleft()
        # keywords 
        if raw_token in self.lexical_element.keywords():
            self.token_type = self.lexical_element.keywords.get(raw_token)
        # symbol 
        elif raw_token[0] in self.lexical_element.symbol(): # 判断第一个元素
            self.token_type = "SYMBOL"
            if len(raw_token)>=2 and raw_token[:2] in ["==",">=","<="]:
                self.current_token = raw_token[:2]
                self.recycle_rest(2,raw_token)
            else:
                self.current_token = raw_token[0]
                self.recycle_rest(1,raw_token)
        # constant int
        elif raw_token[0].isdigit():
            self.token_type = 'INT_CONSTANT'
            end = re.search(r"\d*",raw_token).end()#search the end pos of a sequence of number
            self.current_token = raw_token[:end]
            self.recycle_rest(end,raw_token)
        elif raw_token[0] == '"':
            # 并非只有")这种情况，实际上可以匹配到左引号
            # 因为xxx.("这种情况的前半部分已经被消耗了
            self.token_type = "STRING_CONSTANT"
            # 注意，引号不属于字符串
            end = re.search(r'"\w*"?',raw_token).end()
            # "abcde")
            # "abcd"
            # "abcd 
            if end == len(raw_token):
                if raw_token[-1]=='"': #"abcd"
                    self.current_token = raw_token[1:-1]
                else: #"abcd
                    temp_str = raw_token[1:] 
                    while True: 
                        next = self.raw_tokens.popleft()
                        end = re.search(r'\w*"?',raw_token).end()
                        if end == len(next):
                            if next[end]!='"':
                                temp_str+=next
                                continue
                            else:
                                temp_str+=next[:-1]
                                break
                        else:
                            temp_str+=next[:end]
                            break
                    self.current_token = temp_str
                    self.recycle_rest(end,next)
            else: # "abcde")
                self.current_token = raw_token[1:end] 
                self.recycle_rest(end,raw_token)
        else:
            pass

        return self.current_token

    def recycle_rest(self,pos,buffer):
        """
        将剩下的部分（如果有的话）放回到队列中
        """
        if buffer[pos:] : 
            self.raw_tokens.appendleft(buffer[pos:])

    def token_type(self):
        return self.token_type 

    def keyword(self):
        return self.lexical_element.keywords.get(self.current_token) 

    def symbol(self):
        return self.current_token
    
    def identifier(self):
        return self.current_token
    
    def int_val(self):
        return int(self.current_token)

    def string_val(self):
        return self.current_token



class LexicalElement(object):
    def __init__(self):
        self.keywords = {
                'class': 'CLASS',
                'constructor': 'CONSTRUCTOR',
                'function': 'FUNCTION',
                'method': 'METHOD',
                'field': 'FIELD',
                'static': 'STATIC',
                'var': 'VAR',
                'int': 'INT',
                'char': 'CHAR',
                'boolean': 'BOOLEAN',
                'void': 'VOID',
                'true': 'TRUE',
                'false': 'FALSE',
                'null': 'NULL',
                'this': 'THIS',
                'let': 'LET',
                'do': 'DO',
                'if': 'IF',
                'else': 'ELSE',
                'while': 'WHILE',
                'return': 'RETURN'
            }
        self.symbol = set([
                '{',
                '}',
                '(',
                ')',
                '[',
                ']',
                '.',
                ',',
                ';',
                '+',
                '-',
                '*',
                '/',
                '&',
                '|',
                '<',
                '>',
                '=',
                '~',
            ])

        @property
        def keywords(self):
            return self.keywords

        @property
        def symbol(self):
            return self.symbol