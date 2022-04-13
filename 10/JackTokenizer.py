import re 
from collections import deque

class Token(object):
    def __init__(self,_name=None,_type=None):
        self.name = _name
        self.type =_type 

    def __str__(self):
        return "{: <25}:  {: <30}".format(self.name,self.type)
    

class JackTokenizer(object):
    """
    实例化的时候即完成文件的读取和token列表的创建
    外部模块只能通过get_tokens()获取生成好的token列表
    """
    def __init__(self,filename):
        self.buffer = self._read_file(filename) 
        self.lexical_element = LexicalElement() #mapping table
        self.tokens = self._generate_tokens()

    #### API   ####
    def get_tokens(self):
        return self.tokens
    #### End ######


    def _read_file(self,filename):
        """
        逐行读取文件，对于有效的代码行，按空格分割后作为原始token放入待处理队列
        1. 忽略空行
        2. 忽略注释，包括多行注释，单行注释和行内注释
        """
        in_comment = False
        _buffer = deque() # processing buffer
        with open(filename,"r") as f:
            for line in  f.readlines():
                line = line.strip().split("//")[0]# ignore inline comments 
                if not in_comment:
                    # single line comment
                    if line.startswith("//") or (line.startswith("/*") and line.endswith("*/")):
                        pass
                    # multi line comment start
                    elif line.startswith("/*"):
                        in_comment = True
                    elif line !='':
                        _buffer.extend(line.split()) # split the code line to raw tokens
                # multi line comment end
                elif line.startswith("*/") or line.endswith("*/"):
                        in_comment = False
                else:#multi line comments content
                    pass

        return _buffer
    
    def _generate_tokens(self):
        tokens = []
        while self.buffer:
            tokens.append(self._advance())
        return tokens

    def _advance(self):
        """
        处理buffer，根据实际情况，
        进行再次切分或重组，返回的结果是一个合法的token
        """
        raw_token = self.buffer.popleft()
        token = Token()
       
        # symbol 
        if raw_token[0] in self.lexical_element.symbol: # 判断第一个元素
            token.type = "SYMBOL"
            if len(raw_token)>=2 and raw_token[:2] in ["==",">=","<="]:
                token.name = raw_token[:2]
                self._recycle_rest(2,raw_token)
            else:
                token.name = raw_token[0]
                self._recycle_rest(1,raw_token)
        # constant int
        elif raw_token[0].isdigit():
            token.type = 'INT_CONSTANT'
            end = re.search(r"\d*",raw_token).end()#search the end pos of a sequence of number
            token.name = raw_token[:end]
            self._recycle_rest(end,raw_token)
        elif raw_token[0] == '"':
            # 并非只有")这种情况，实际上可以匹配到左引号
            # 因为xxx.("这种情况的前半部分已经被消耗了
            token.type = "STRING_CONSTANT"
            # 注意，引号不属于字符串
            # "abcde")
            # "abcd"
            # "abcd 
            is_first = True
            temp_str = ""
            while True: 
                if is_first:
                    raw_token = raw_token[1:]
                    is_first = False
                pos = raw_token.find('"')
                if pos == -1:
                    temp_str = temp_str + raw_token + " "
                else:
                    temp_str = temp_str + raw_token[:pos]
                    self._recycle_rest(pos+1,raw_token)
                    break
                raw_token = self.buffer.popleft()
            token.name = temp_str

        else: # keywords  and identifier 以字符串的形式存在，可能会被符号分割而且不方便直接搜索，依次比较比较好
            token.name = raw_token
            for pos, ele in enumerate(raw_token):
                if ele in self.lexical_element.symbol:
                    token.name = raw_token[:pos]
                    self._recycle_rest(pos,raw_token)
                    break
            if token.name in self.lexical_element.keywords:
                token.type = 'KEYWORD'
            else:
                token.type = 'IDENTIFIER'
        
        return token

    def _recycle_rest(self,pos,buf):
        """
        将剩下的部分（如果有的话）放回到队列中
        """
        if buf[pos:] : 
            self.buffer.appendleft(buf[pos:])


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