from functools import wraps
import traceback
from SymbolTable import SymbolTable
from VMWriter import VMWriter

CLASS_VAR_DEC_TOKENS = [ "static", "field" ]
SUBROUTINE_TOKENS = [ "function", "method", "constructor" ]
STATEMENT_TOKENS = [ 'do', 'let', 'while', 'return', 'if' ]
OPERATORS = [
        '+',
        '-',
        '*',
        '/',
        '&',
        '|',
        '<',
        '>',
        '='
    ]
UNARY_OPERATORS = [ '-', '~' ]
ARITHMETIC = {
'+': 'add',
'-': 'sub',
'=': 'eq',
'>': 'gt',
'<': 'lt',
'&': 'and',
'|': 'or'
}

ARITHMETIC_UNARY = {
'-': 'neg',
'~': 'not'
}
class CompilationEngine(object):
    def __init__(self,jackfile,type="XML"):
        self.jackfile = jackfile
        self.xmlfile = self.jackfile.replace(".jack","T-my.xml") if type == "TXML" else self.jackfile.replace(".jack","-my.xml")
        self.tokens = None
        self.index = 0
        self.current = None
        self.indent = 0
        self.symbol_table = SymbolTable(self.jackfile.replace(".jack",".symbol.json"))
        self.vm_writer = VMWriter(self.jackfile.replace(".jack",".vm"))
        self.class_name = None
        ## for unique labels
        self.while_label_idx = 0
        self.if_label_idx = 0

    def __enter__(self):
        print("Open file ",self.xmlfile)
        self.xml = open(self.xmlfile,'w')
        return self

    def __exit__(self,exc_type,exc_val,exc_tb):
        self.xml.close()
        print("CompilationEngine exit, close ",self.xmlfile)
        print("Dump Symbol Table",self.symbol_table.dump())
        
        if exc_val:
            print("exit:", exc_type, exc_val, exc_tb)
            print(traceback.print_tb(exc_tb))
        return True

    def print_tokens(self):
        for token in self.tokens:
            print(token)

    def set_tokens(self,tokens):
        """
        存放由 Tokenizer 创建的 tokens 
        """
        self.tokens = tokens

    def has_more_tokens(self):
        return self.index < len(self.tokens)

    def get_next(self):
        if self.has_more_tokens():
            self.current = self.tokens[self.index]
            self.index +=1

    def peek_next(self):
        if self.has_more_tokens():
            next_token = self.tokens[self.index]
            return next_token.name
    def peek_next_type(self):
        if self.has_more_tokens():
            next_token = self.tokens[self.index]
            return next_token.type

    def tagger(tag=None): 
        """
        装饰compile_x函数，在其前后自动添加对应的tag
        定义接收参数的装饰器 tagge 接收tag参数并返回一个接收func参数的deco，
        然后func通过deco传递进wrapper进行包装，被包装的函数会传入self
        # func = tagger(tag="class")(func(self))
        https://python3-cookbook.readthedocs.io/zh_CN/latest/c09/p04_define_decorator_that_takes_arguments.html
        """
        def deco(func):
            @wraps(func) #确保函数名正确
            def wrapper(self, *args, **kwargs):
                self.write_non_terminal_tag(tag)
                self.increase_indent()
                ret = func(self, *args, **kwargs)
                self.decrease_indent()
                self.write_non_terminal_tag("/"+tag)
                return ret
            return wrapper
        return deco
    
    def compile_jackfile(self):
        """
        对jack文件进行编译，首先需要创建文件作用域的static符号表
        然后从唯一的根节点 class 开始编译
        """
        # 创建文件全局作用域 static 符号表
        self.symbol_table.create_table(self.jackfile.split("/")[-1],"static")
        # class is the only root
        self.compile_class() 
        self.vm_writer.close()

    @tagger(tag="class")
    def compile_class(self):
        """
        'class' className '{' classVarDec* subroutineDec* '}' 
        """
        self.write_next_token() # class
        class_name_token = self.write_next_token() # className
        self.class_name = class_name_token.name
        # create class scope symbol table (field)
        self.symbol_table.create_table("class",self.class_name) 
        self.write_next_token() # "{"
        
        while self.peek_next() in CLASS_VAR_DEC_TOKENS: # classVarDec*
            self.compile_class_var_dec()

        while self.peek_next() in SUBROUTINE_TOKENS:  # subroutineDec
            self.compile_subroutineDec()
       
        self.write_next_token() # "}"


    @tagger(tag="classVarDec")
    def compile_class_var_dec(self):
        """
        ('static' | 'field' ) type varName (',' varName)* ';'
        类变量声明语句，只添加符号到符号表，不需要写vmcode
        """
        kind_token = self.write_next_token() # 'static' | 'field' 
        type_token = self.write_next_token() # type
        varName_token = self.write_next_token() # varName
        
        # 添加变量到符号表
        self.symbol_table.define(varName_token.name,type_token.name,kind_token.name.upper())
        # while self.current.name != ";":
        #     self.write_next_token()
        # 两种不同的写法，上面一种判断结束符，只要不是结束就写，不关心写的是什么
        # 但是必须要使用当前的token来进行判断
        # 下面的写法，是判断是否还要继续写，如果写的话，每一步都有明确的含义。
        # 本程序使用了下面这种写法，可读性更好一些，也容易调试。
        # 即统一使用下一个token，判断是否还要继续处理，明确当前打印的元素属于语法的哪个部分
        # ？使用if判断，*使用while判断
        while self.peek_next() == ",": # (',' varName)*
            self.write_next_token() # ","
            varName_token = self.write_next_token() # "varName"
            self.symbol_table.define(varName_token.name,type_token.name,kind_token.name.upper())
        
        self.write_next_token()#;

    @tagger(tag="subroutineDec")
    def compile_subroutineDec(self):
        """
        'constructor' | 'function' | 'method' 'void' | type subroutineName '('parameterList ')' subroutineBody
        声明语句，只需要添加符号表
        """
        
        kind_token = self.write_next_token()         # ('constructor' | 'function' | 'method')
        self.write_next_token()         # ('void' | type)
        subroutine_name_token = self.write_next_token()         # subroutineName
        # 进入新的函数作用域
        self.symbol_table.start_subroutine(subroutine_name_token.name,self.class_name)

        if kind_token.name != "function":
            self.symbol_table.define("this",self.class_name,"ARG")
        
        self.write_next_token()         # '('
        self.compile_parameter_list()
        self.write_next_token()         # ')'
        self.compile_subroutine_body(subroutine_name_token.name,kind_token.name)

        
        self.symbol_table.end_subroutine()

    @tagger(tag="subroutineBody")
    def compile_subroutine_body(self,name,kind):
        """
        '{' varDec* statements '}'
        函数体，包含局部变量声明（创建符号表）和函数体语句（写VMcode）
        """
        self.write_next_token() #{
        
        while self.peek_next() == "var":
            self.compile_var_dec()
        
        if self.peek_next() in STATEMENT_TOKENS:
            self.compile_statements()

        ## 输出一般函数实现指令
        ## function name nargs，函数foo的实现，使用nargs个局部变量
        function_name = '{}.{}'.format(self.class_name, name)
        nlocals = self.symbol_table.var_count('VAR') # 获取局部变量个数
        self.vm_writer.write_func(function_name, nlocals)
        
        ## 对于 构造函数和类方法，有额外的操作
        if kind == 'constructor':
            num_fields = self.symbol_table.var_count('FIELD')
            self.vm_writer.write_push('CONST', num_fields)
            self.vm_writer.write_call('Memory.alloc', 1)
            self.vm_writer.write_pop('POINTER', 0)
        elif kind == 'method':
            self.vm_writer.write_push('ARG', 0)
            self.vm_writer.write_pop('POINTER', 0)

        self.write_next_token()# }

    @tagger(tag="parameterList")
    def compile_parameter_list(self):
        """
        (( type varName ) ( "," type varName )*)?
        参数列表，属于声明的一种，只需要创建符号表
        """
        if self.peek_next() != ")": # 可能没有参数
            type_token = self.write_next_token() # type
            varname_token = self.write_next_token() # varName
            self.symbol_table.define(varname_token.name,type_token.name,"ARG")

        while self.peek_next() != ")":
            self.write_next_token() # ,
            type_token = self.write_next_token() # type
            varname_token = self.write_next_token() # varName
            self.symbol_table.define(varname_token.name,type_token.name,"ARG")

    @tagger(tag="varDec")
    def compile_var_dec(self):
        """
        'var' type varName (',' varName)* ';'
        函数内部变量声明，只需要创建符号表
        """
        self.write_next_token() # var
        type_token = self.write_next_token() # type
        varname_token = self.write_next_token() # varName

        self.symbol_table.define(varname_token.name,type_token.name,"VAR")

        while self.peek_next() == ",":
            self.write_next_token() # ,
            varname_token = self.write_next_token() # varName
            self.symbol_table.define(varname_token.name,type_token.name,"VAR")

        self.write_next_token() # ;
    
    @tagger(tag="statements")
    def compile_statements(self):
        while self.peek_next() != "}": # ending for statements. for each statement based on thier own
            if self.peek_next() == "let":
                self.compile_let()
            elif self.peek_next() == "if":
                self.compile_if()
            elif self.peek_next() == "while":
                self.compile_while()
            elif self.peek_next() == "do":
                self.compile_do()
            elif self.peek_next() == "return":
                self.compile_return()
            
    @tagger(tag="letStatement")
    def compile_let(self):
        """
        "let" varName ( "[" expr "]" )? "=" expr ";"
        赋值语句，需要写vmcode
        数组访问操作：
        push arr // base address 将数组基地址压栈
        {{vm code computing and pushing expr1}}
        add // top stack value = RAM address of arr[expr1]
        {{vm code computing and pushing expr2}}
        pop temp 0 // temp 0 = the value of expr2 ，即将表达式2的求值结果暂存到 temp 0
                              // top stack value = RAM address of arr[expr2]
        pop pointer 1 // 将计算结果赋值为 THAT，将that段对齐到arr[2]
        push temp 0  // 表达式 expr2 的结果
        pop that 0  // 对that 0赋值，以实现对arr[expr1]赋值
        """
        self.write_next_token() #let
        var_name_token = self.write_next_token() #varName
        kind = self.symbol_table.kindof(var_name_token.name)
        index = self.symbol_table.indexof(var_name_token.name)

        if self.peek_next() == "[": # 数组访问
            self.write_next_token() # "["
            self.vm_writer.write_push(kind, index) # push arr
            self.compile_expression() # expr1 求值
            self.write_next_token() # "]"

            self.vm_writer.write_arithmetic('ADD')  # add

            self.write_next_token() # "="
            self.compile_expression() # expr2 求值
            self.write_next_token() # ";"
            
            self.vm_writer.write_pop('TEMP', 0) # pop temp 0 存放 expr2结果到TEMP段
            self.vm_writer.write_pop('POINTER', 1) # pop pointer 1
            self.vm_writer.write_push('TEMP', 0) # push temp 0
            self.vm_writer.write_pop('THAT', 0) # pop that 0
        else: # 普通表达式求值
            self.write_next_token() # "="
            self.compile_expression()
            self.write_next_token() # ";"

            self.vm_writer.write_pop(kind, index) # 表达式结果存放到 kind 段


    @tagger(tag="ifStatement")
    def compile_if(self):
        """
        "if" "(" expr ")" "{" statements "}" ("else" "{" statements "}" )? 
        代码生成逻辑
        	compiled（expr)
            not
            if-goto IF_FALSE
            compiled (statement1)
            goto IF_END
        label IF_FALSE
        compiled (statement2)
        label IF_END
        """
        self.if_label_idx += 1
        self.write_next_token()     # if
        self.write_next_token()     # '('
        self.compile_expression()    # expression  # compiled（expr)
        self.write_next_token()     # ')'
        self.write_next_token()     # '{'

        self.vm_writer.write_arithmetic('NOT') # not

        self.vm_writer.write_if('IF_FALSE_{}\n'.format(self.if_label_idx)) # if-goto IF_FALSE
        
        self.compile_statements()    # statements 1 

        self.vm_writer.write_goto('IF_END_{}\n'.format(self.if_label_idx)) # goto IF_END

        self.write_next_token()     # '}'
        
        
        if self.peek_next() == "else":
            self.write_next_token()     # 'else'
            self.write_next_token()     # '{'
            self.vm_writer.write_label('IF_FALSE_{}\n'.format(self.if_label_idx)) # label IF_FALSE
            self.compile_statements()    # statements 2
            self.write_next_token()     # '}'
    
        self.vm_writer.write_label('IF_END_{}\n'.format(self.if_label_idx))

    @tagger(tag="whileStatement")
    def compile_while(self):
        """
        "while" "(" expr ")" "{" statements "}"
        代码生成逻辑
        label WHILE_START
            compiled(expr)
            not 考虑到if -goto的语义是跳转而非进入，这里必须取反
            if-goto WHILE_START_END
            compiled(statement)
            goto WHILE_START
        label WHILE_START_END
        """
        self.while_label_idx += 1
        
        self.vm_writer.write_label('WHILE_START_{}\n'.format(self.while_label_idx)) # label WHILE_START

        self.write_next_token()     # 'while'
        self.write_next_token()     # '('
        self.compile_expression() # compiled(expr)

        self.vm_writer.write_arithmetic('NOT') # 
        self.write_next_token()     # ')'
        self.write_next_token()     # '{'

        self.vm_writer.write_if('WHILE_END_{}\n'.format(self.while_label_idx)) # if-goto WHILE_START_END

        self.compile_statements()    # statements 
        self.vm_writer.write_goto('WHILE_START_{}\n'.format(self.while_label_idx)) # goto WHILE_START
        self.vm_writer.write_label('WHILE_END{}\n'.format(self.while_label_idx)) # label WHILE_START_END

        self.write_next_token()     # '}'


    @tagger(tag="doStatement")
    def compile_do(self):
        """
        "do" subroutineCall ";"
        do 语句不关心函数的返回值，但是此时返回值在栈顶，必须要将其pop掉
        """
        self.write_next_token() #do
        token = self.write_next_token() # subroutineName or ( className | varName)
        self.subroutine_call(token.name)
        self.vm_writer.write_pop('TEMP', 0) # pop temp 0 丢弃返回值
        self.write_next_token() # ;

    @tagger(tag="returnStatement")
    def compile_return(self):
        """
        "return" expr? ";"
        return 语句如果不返回任何值，则编译器必须返回0作为默认值
        """

        self.write_next_token() # return
        if self.peek_next() != ";":
            self.compile_expression()
        else: # 无返回值
            self.vm_writer.write_push("CONST",0) # push constant 0

        self.write_next_token() # ;

    def subroutine_call(self,identifier):
        """
        subroutineName '(' expressionList ')' | ( className | varName) '.' subroutineName '(' expressionList ')'
        不是子节点，不需要加tag
        """
        # 特殊处理，将subroutineName或者( className | varName) 拿到外面写
        # self.write_next_token() # subroutineName or ( className | varName)
        nargs = 0
        if self.peek_next() == "(":
            function_name = '{}.{}'.format(self.class_name, identifier)
            nargs += 1
            self.vm_writer.write_push('POINTER', 0)
            
        elif self.peek_next() == ".":
            self.write_next_token() # "."
            method_token = self.write_next_token() # "subroutineName"
            type = self.symbol_table.typeof(identifier)
            if type : 
                kind = self.symbol_table.kindof(identifier)
                index = self.symbol_table.indexof(identifier)

                self.vm_writer.write_push(kind, index)
                function_name = '{}.{}'.format(type, method_token.name)
                nargs += 1
            else: # it's a class
                class_name = identifier
                function_name = '{}.{}'.format(class_name, method_token.name)

        self.write_next_token() # "("
        nargs += self.compile_expression_list()
        self.write_next_token() # ")"
        
        self.vm_writer.write_call(function_name, nargs)

        


    @tagger(tag="expression")
    def compile_expression(self):
        """
        term (op term)*
        """
        self.compile_term()
        while self.peek_next() in OPERATORS:
            op_token = self.write_next_token()
            op = op_token.name
            self.compile_term()
            if op in ARITHMETIC.keys():
                self.vm_writer.write_arithmetic(ARITHMETIC[op])
            elif op == '*':
                self.vm_writer.write_call('Math.multiply', 2)
            elif op == '/':
                self.vm_writer.write_call('Math.divide', 2)

    @tagger(tag="expressionList")
    def compile_expression_list(self):
        """
        (expression (',' expression)* )? 
        """
        # 在父节点中读到 ( 进入该函数，由于expressionList可能为空，不能默认调用一次expr
        # 读取下一个 token，如果不是终止符号，才调用 expr
        nargs = 0
        if self.peek_next() != ")":
            nargs +=1
            self.compile_expression()
        
        while self.peek_next() != ")":
            nargs += 1
            self.write_next_token()
            self.compile_expression()
        
        return nargs
    
    @tagger(tag="term")
    def compile_term(self):
        """
        unaryOp term |
        integerConstant | stringConstant | keywordConstant | varName | 
        varName '[' expression']' | 
        subroutineCall: subroutineName '(' expressionList ')' | ( className | varName) '.' subroutineName '(' expressionList ')'
        '(' expression ')' | 
        """
        
        if self.peek_next() in UNARY_OPERATORS:  #unaryOp term 
            op_token = self.write_next_token() # unaryOP
            self.compile_term() # term
            self.vm_writer.write_arithmetic(ARITHMETIC_UNARY[op_token.name])
        elif self.peek_next() == "(": #'(' expression ')' 
            self.write_next_token() #(
            self.compile_expression() # expr
            self.write_next_token() # )
        elif self.peek_next_type() == "INT_CONSTANT":# if exp is number n:
            int_token = self.write_next_token()
            self.vm_writer.write_push('CONST', int_token.name) # push const n
        elif self.peek_next_type() == "STRING_CONSTANT":
            string_token = self.write_next_token()
            self.vm_writer.write_push('CONST', len(string_token.name))
            self.vm_writer.write_call('String.new', 1)
            for char in string_token.name:
                self.vm_writer.write_push('CONST', ord(char))
                self.vm_writer.write_call('String.appendChar', 2)
        elif self.peek_next_type() ==  "KEYWORD":
            keyword_token = self.write_next_token()
            if keyword_token.name == 'this':
                self.vm_writer.write_push('POINTER', 0)
            else:
                self.vm_writer.write_push('CONST', 0)
            if keyword_token.name == 'true':
                self.vm_writer.write_arithmetic('NOT')
        else: #identifier (varName | varName[] \ subroutineCall )
            var_name_token = self.write_next_token() #  varName 
            if self.peek_next() == "[": # varName[]  
                self.write_next_token() # "["
                self.compile_expression()  # expr
                self.write_next_token() # "]"
                kind = self.symbol_table.kindof(var_name_token.name)
                index = self.symbol_table.indexof(var_name_token.name)
                self.vm_writer.write_push(kind, index)

                self.vm_writer.write_arithmetic('ADD')
                self.vm_writer.write_pop('POINTER', 1)
                self.vm_writer.write_push('THAT', 0)
            elif self.peek_next() == "(" or self.peek_next() == ".": # subroutineCall
                self.subroutine_call(var_name_token.name)
            else: # varName but write already
                # 只需要生成代码，xml 已经写完了
                kind  = self.symbol_table.kindof(var_name_token.name)
                index = self.symbol_table.indexof(var_name_token.name)
                self.vm_writer.write_push(kind, index)

    
    def write(self,_xml):
        self.xml.write(_xml)
    
    def write_next_token(self):
        self.get_next()
        token = self.current
        if token.type == 'KEYWORD':
            self.write_terminal_tag(token.name,'keyword')
        elif token.type == 'SYMBOL':
            self.write_terminal_tag(token.name,'symbol')
        elif token.type == 'INT_CONSTANT':
            self.write_terminal_tag(token.name,'integerConstant')
        elif token.type == 'STRING_CONSTANT':
            self.write_terminal_tag(token.name,'stringConstant')
        elif token.type == 'IDENTIFIER':
            self.write_terminal_tag(token.name,'identifier')
        
        return token

    def write_terminal_tag(self,token,tag):
        """
        <keyword>class</keyword>
        """
        token = token.replace('&', '&amp;')
        token = token.replace('<', '&lt;')
        token = token.replace('>', '&gt;')
        self.write("{indent}<{tag}> {token} </{tag}>\n".format(tag=tag,
                                                                                                    token=token,
                                                                                                    indent="\t"*self.indent))
    
    def write_non_terminal_tag(self,tag):
        """
        <class>
        or 
        </class>
        """
        self.write("{indent}<{tag}>\n".format(tag=tag,indent="\t"*self.indent))
            

    def increase_indent(self):
        self.indent += 1
    
    def decrease_indent(self):
        self.indent -= 1