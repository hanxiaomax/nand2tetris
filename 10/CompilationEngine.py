import traceback

TERMINAL_TOKEN_TYPES = ["SYMBOL", "STRING_CONSTANT", "INT_CONSTANT", "IDENTIFIER"]
TYPE_KEYWORD = [ "boolean", "class", "void", "int" ]
## Entry in class
CLASS_VAR_DEC_TOKENS = [ "static", "field" ]
SUBROUTINE_TOKENS = [ "function", "method", "constructor" ]
#####

STATEMENT_TOKENS = [ 'do', 'let', 'while', 'return', 'if' ]
EXPR_START_TOKENS= [
                                        "[",
                                        "(",
                                        "=",
                                        ]

EXPR_END_TOKENS = [
                                            ";",
                                            ")",
                                            "]",
                                            ","
                                        ]
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

class CompilationEngine(object):
    def __init__(self,jackfile,type="XML"):
        self.xmlfile = jackfile.replace(".jack","T-my.xml") if type == "TXML" else jackfile.replace(".jack","-my.xml")
        self.tokens = None
        self.index = 0
        self.curr_token = None
        self.token_type = None
    
    def print_tokens(self):
        for t in self.tokens:
            print("{: <25}:  {: <30}".format(t.token,t.type))

    def set_tokens(self,tokens):
        self.tokens = tokens
    
    def has_more_tokens(self):
        return self.index < len(self.tokens)

    def get_next(self):
        self.curr_token, self.token_type = self.tokens[self.index]
        self.index +=1
    
    def peek_next(self):
        next = self.tokens[self.index].token
        return next

    def __enter__(self):
        print("Open file ",self.xmlfile)
        self.xml = open(self.xmlfile,'w')
        return self

    def __exit__(self,exc_type,exc_val,exc_tb):
        self.xml.close()
        print("CompilationEngine exit, close ",self.xmlfile)
        if exc_val:
            print("exit:", exc_type, exc_val, exc_tb)
            print(traceback.print_tb(exc_tb))
        return True

    def tagger(func=None,tag=None):
        def deco(func):
            def wrapper(self, *args, **kwargs):
                self.write_tag(tag)
                func(self)
                self.write_tag("/"+tag)
            return wrapper
        return deco

    def write_token(self,token,token_type):
        token = token.replace('&', '&amp;')
        token = token.replace('<', '&lt;')
        token = token.replace('>', '&gt;')

        self.write('<' + token_type + '> ')
        self.write(token)
        self.write(' </' + token_type + '>\n')
    
    def write_tag(self,tag):
        self.write(' <' + tag + '>\n')

    def write(self,_xml):
        self.xml.write(_xml)

    @tagger(tag="class")
    def compile_class(self):
        """
        'class' className '{' classVarDec* subroutineDec* '}' 
        """
        while self.curr_token!="}":
            self.get_next() 
            if self.curr_token in CLASS_VAR_DEC_TOKENS: # classVarDec*
                self.compile_class_var_dec()
            elif self.curr_token in SUBROUTINE_TOKENS: # 
                self.compile_subroutineDec()
            elif self.curr_token!="}":
                self.write_terminal_token()
        # 结束符属于本节点
        self.write_terminal_token()# } 

    @tagger(tag="classVarDec")
    def compile_class_var_dec(self):
        """
        语法： ('static' | 'field' ) type varName (',' varName)* ';'
        父节点： subroutineDec
        子节点：没有子节点，遇到结束符返回到父节点。
        起始： CLASS_VAR_DEC_TOKENS
        终止：";"
        """
        self.write_terminal_token() #起始符号属于子节点，子节点中写
        while self.curr_token != ";":
            self.get_next()
            self.write_terminal_token()
            
    @tagger(tag="subroutineDec")
    def compile_subroutineDec(self):
        """
        语法： 'constructor' | 'function' | 'method' 'void' | type subroutineName '('parameterList ')' "{"subroutineBody"}"
        父节点： subroutineDec
        子节点： parameterlist / subroutinebody
        起始："{" 属于本节点
        终止："}" 属于父节点
        """
        self.write_terminal_token()#起始符号属于子节点，子节点中写
        while self.curr_token != "}":
            self.get_next()
            if self.curr_token == "(": # parameterlist 起始符号为左括号
                self.write_terminal_token() #(
                self.compile_parameter_list() #parameterlist 的起始和结束括号都属于父节点
                self.write_terminal_token() #)
            elif self.curr_token == "{": # subroutinebody 起始符号为大括号
                self.compile_subroutine_body()
            else:#elif self.curr_token != "}":
                self.write_terminal_token()
        # 终止符号属于父节点
    
    @tagger(tag="subroutineBody")
    def compile_subroutine_body(self):
        """
        语法：'{' varDec* statements '}'
        父节点： subroutineDec
        子节点： varDec / statements
        起始："{" 属于本节点
        终止："}" 属于本节点
        """
        self.write_terminal_token() #{
        while self.curr_token != "}":
            self.get_next()
            if self.curr_token == "var":
                self.compile_var_dec()
            elif self.curr_token in STATEMENT_TOKENS:
                self.compile_statements()
            else:
                self.write_terminal_token()
        self.write_terminal_token()# }

    @tagger(tag="parameterList")
    def compile_parameter_list(self):
        """
        语法：(( type varName ) ( "," type varName )*)?
        父节点： subroutineDec
        子节点：无子节点
        起始："("
        终止：")"
        起始符号和终止符号均为括号，但属于父节点，在父节点中写
        """
        while self.has_more_tokens():
            self.get_next()
            if self.curr_token != ")": #遇到终止符号返回父节点，但是在该节点中写
                self.write_terminal_token()
            else:
                return 

    @tagger(tag="varDec")
    def compile_var_dec(self):
        """
        语法：'var' type varName (',' varName)* ';'
        父节点： subroutinebody
        子节点：无子节点
        起始："var"
        终止：";"
        """
        self.write_terminal_token()
        while self.curr_token != ";":
            self.get_next()
            self.write_terminal_token()
    
    @tagger(tag="statements")
    def compile_statements(self):
        """
        语法：'var' type varName (',' varName)* ';'
        父节点： subroutinebody
        子节点： let / if / while / do / return 
        起始： STATEMENT_TOKENS
        终止：} 
        起始符号属于各子节点，所以不再父节点中写。终止符号属于父节点
        """
        while self.curr_token != "}": # ending for statements. for each statement based on thier own
            if self.curr_token == "let":
                self.compile_let()
            elif self.curr_token == "if":
                self.compile_if()
            elif self.curr_token == "while":
                self.compile_while()
            elif self.curr_token == "do":
                self.compile_do()
            elif self.curr_token == "return":
                self.compile_return()
            else:
                self.write_terminal_token()
            self.get_next()
            
    @tagger(tag="letStatement")
    def compile_let(self):
        """
        语法："let" varName ( "[" expr "]" )? "=" expr ";"
        父节点： statements
        子节点： expr
        起始： let
        终止：";"
        """
        self.write_terminal_token() #let
        while self.curr_token != ";":
            self.get_next()
            if self.curr_token in EXPR_START_TOKENS : 
                self.write_terminal_token()
                self.compile_expression()
                self.write_terminal_token()
            elif self.curr_token!=";" :#and self.curr_token not in EXPR_END_TOKENS:
                self.write_terminal_token() #打印除了结束符之外的其他元素


    @tagger(tag="ifStatement")
    def compile_if(self):
        """
        语法："if" "(" expr ")" "{" statements "}" ("else" "{" statements "}" )? 
        父节点： statements
        子节点： expr / statements
        起始： if
        终止："}"
        """
        self.write_terminal_token()
        while self.curr_token != "}":
            self.get_next()
            if self.curr_token in EXPR_START_TOKENS : 
                self.write_terminal_token()
                self.compile_expression()
                self.write_terminal_token()
            elif self.curr_token in STATEMENT_TOKENS:
                self.compile_statements()
            else:
                self.write_terminal_token()
        self.write_terminal_token()


    @tagger(tag="whileStatement")
    def compile_while(self):
        """
        语法："while" "(" expr ")" "{" statements "}"
        父节点： statements
        子节点： expr / statements
        起始： while
        终止："}"
        """
        self.write_terminal_token()
        while self.curr_token != "}":
            self.get_next()
            if self.curr_token == "(":
                self.write_terminal_token()
                self.compile_expression()
                self.write_terminal_token()
            elif self.curr_token in STATEMENT_TOKENS :
                self.compile_statements()
            else:
                self.write_terminal_token()
        self.write_terminal_token()

    @tagger(tag="doStatement")
    def compile_do(self):
        """
        语法："do" subroutineCall ";"
        父节点： statements
        子节点： expr  / exprList (subroutineCall不属于子节点，属于类型定义)
        起始： do
        终止：";"
        """
        self.write_terminal_token()#do
        self.subroutine_call()
        while self.curr_token != ";":
            self.get_next()
            self.write_terminal_token()

    def subroutine_call(self):
        """
        不是子节点，不需要加tag
        """
        while self.curr_token != ")":
            self.get_next()
            if self.curr_token == "(": # exprlist的起始符号
                self.write_terminal_token()
                self.compile_expression_list()
            elif self.curr_token!=")":
                self.write_terminal_token()
        self.write_terminal_token()

    @tagger(tag="returnStatement")
    def compile_return(self):
        """
        语法："return" expr? ";"
        父节点： statements
        子节点： expr
        起始： return
        终止：";"
        """
        self.write_terminal_token() #return 
        if self.peek_next()!= ";": #如果return后面不是分号，则肯定是表达式
            self.compile_expression()
        while self.curr_token != ";": 
            self.get_next() 
            self.write_terminal_token() 

    @tagger(tag="expression")
    def compile_expression(self):
        """
        语法：term (op term)*
        父节点： let / if / while / return / term /subroutineCall
        子节点： term
        起始： EXPR_START_TOKENS = ["[", "(" ,"="]`
        终止： EXPR_END_TOKENS = [";", ")", "]"]
        起始符号和结束符号均属于父节点
        """
        self.get_next()
        self.compile_term()
        
        while self.peek_next() in OPERATORS:
            self.get_next()
            self.compile_term()
        # while self.curr_token not in EXPR_END_TOKENS:
        #     self.get_next()
        #     if self.curr_token in OPERATORS: 
        #         self.write_terminal_token() # operator
        #         self.get_next()
        #         self.compile_term()
                
        

            
    @tagger(tag="expressionList")
    def compile_expression_list(self):
        """
        语法：(expression (',' expression)* )? 
        父节点： do / term
        子节点： expr
        起始： (
        终止：)
        起始和终止符号都属于父节点
        """
        # 在父节点中读到 ( 进入该函数，由于expressionList可能为空，不能默认调用一次expr
        # 读取下一个 token，如果不是终止符号，才调用 expr
        if self.peek_next() == ")":
            return 
        while self.curr_token != ")":
            self.compile_expression()
    
    @tagger(tag="term")
    def compile_term(self):
        """
        integerConstant | 
        stringConstant | 
        keywordConstant | 
        varName | 
        varName '[' expression']' | subroutineCall | '(' expression ')' | unaryOp term 
        """
        
        if self.token_type == "IDENTIFIER" :
            if self.peek_next() == "[": # expr
                self.write_terminal_token()
                self.get_next()
                self.write_terminal_token()
                self.compile_expression()
                self.write_terminal_token()
            elif self.peek_next() == "(" or self.peek_next() == ".": #subroutine call
                self.write_terminal_token()
                self.get_next()
                self.write_terminal_token()
                self.subroutine_call()
            else:
                self.write_terminal_token()
        elif self.curr_token in UNARY_OPERATORS:
            self.write_terminal_token()
            self.compile_term()
        else:
            self.write_terminal_token()

    
    def write_terminal_token(self,):
        if self.token_type == 'KEYWORD':
            self.write_token(self.curr_token,'keyword')
        elif self.token_type == 'SYMBOL':
            self.write_token(self.curr_token,'symbol')
        elif self.token_type == 'INT_CONSTANT':
            self.write_token(str(self.curr_token),'integerConstant')
        elif self.token_type == 'STRING_CONSTANT':
            self.write_token(self.curr_token,'stringConstant')
        elif self.token_type == 'IDENTIFIER':
            self.write_token(self.curr_token,'identifier')