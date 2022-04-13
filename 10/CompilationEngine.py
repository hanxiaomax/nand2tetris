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
        self.current = None
    
    def print_tokens(self):
        for token in self.tokens:
            print(token)

    def set_tokens(self,tokens):
        self.tokens = tokens
    
    def has_more_tokens(self):
        return self.index < len(self.tokens)

    def get_next(self):
        if self.has_more_tokens():
            self.current = self.tokens[self.index]
            self.index +=1

    def write_next_token(self):
            self.get_next()
            self.write_terminal_token()

    def peek_next(self):
        if self.has_more_tokens():
            next_token = self.tokens[self.index]
            return next_token.name

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
    


    @tagger(tag="class")
    def compile_class(self):
        """
        'class' className '{' classVarDec* subroutineDec* '}' 
        """
        self.write_next_token() # class
        self.write_next_token() # className
        self.write_next_token() # "{"

        while self.peek_next() in CLASS_VAR_DEC_TOKENS: # classVarDec*
            self.compile_class_var_dec()

        while self.peek_next() in SUBROUTINE_TOKENS:  # subroutineDec
            self.compile_subroutineDec()
       
        self.write_next_token() # "}"


    @tagger(tag="classVarDec")
    def compile_class_var_dec(self):
        """
        语法： ('static' | 'field' ) type varName (',' varName)* ';'
        父节点： subroutineDec
        子节点：没有子节点，遇到结束符返回到父节点。
        起始： CLASS_VAR_DEC_TOKENS
        终止：";"
        """
        self.write_next_token() # 'static' | 'field' 
        self.write_next_token() # type
        self.write_next_token() # varName
        
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
            self.write_next_token() # "varName"
        
        self.write_next_token()#;

    @tagger(tag="subroutineDec")
    def compile_subroutineDec(self):
        """
        语法： 'constructor' | 'function' | 'method' 'void' | type subroutineName '('parameterList ')' subroutineBody
        父节点： subroutineDec
        子节点： parameterlist / subroutinebody
        起始："{" 属于父节点
        终止："}" 属于父节点
        """
        self.write_next_token()         # ('constructor' | 'function' | 'method')
        self.write_next_token()         # ('void' | type)
        self.write_next_token()         # subroutineName
        self.write_next_token()         # '('
        self.compile_parameter_list()
        self.write_next_token()         # ')'
        self.compile_subroutine_body()


    @tagger(tag="subroutineBody")
    def compile_subroutine_body(self):
        """
        语法：'{' varDec* statements '}'
        父节点： subroutineDec
        子节点： varDec / statements
        起始："{" 属于本节点
        终止："}" 属于本节点
        """
        self.write_next_token() #{
        
        while self.peek_next() == "var":
            self.compile_var_dec()
        
        if self.peek_next() in STATEMENT_TOKENS:
            self.compile_statements()
 
        self.write_next_token()# }

    @tagger(tag="parameterList")
    def compile_parameter_list(self):
        """
        语法：(( type varName ) ( "," type varName )*)?
        父节点： subroutineDec
        子节点：无子节点
        起始："(" 属于父节点
        终止：")" 属于父节点
        """
        if self.peek_next() != ")": # 可能没有参数
            self.write_next_token() # type
            self.write_next_token() # varName

        while self.peek_next() != ")":
            self.write_next_token() # ,
            self.write_next_token() # type
            self.write_next_token() # varName

    @tagger(tag="varDec")
    def compile_var_dec(self):
        """
        语法：'var' type varName (',' varName)* ';'
        父节点： subroutinebody
        子节点：无子节点
        起始："var"
        终止：";"
        """
        self.write_next_token() # var
        self.write_next_token() # type
        self.write_next_token() # varName

        while self.peek_next() == ",":
            self.write_next_token() # ,
            self.write_next_token() # varName

        self.write_next_token() # ;
    
    @tagger(tag="statements")
    def compile_statements(self):
        """
        语法：
        父节点： subroutinebody
        子节点： let / if / while / do / return 
        起始： STATEMENT_TOKENS
        终止：} 
        """
        
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
        语法："let" varName ( "[" expr "]" )? "=" expr ";"
        父节点： statements
        子节点： expr
        起始： let
        终止：";"
        """
        self.write_next_token() #let
        self.write_next_token() #varName
        if self.peek_next() == "[":
            self.write_next_token() # "["
            self.compile_expression()
            self.write_next_token() # "]"

        self.write_next_token() # "="
        self.compile_expression()
        self.write_next_token() # ";"


    @tagger(tag="ifStatement")
    def compile_if(self):
        """
        语法："if" "(" expr ")" "{" statements "}" ("else" "{" statements "}" )? 
        父节点： statements
        子节点： expr / statements
        起始： if
        终止："}"
        """
        self.write_next_token()     # if
        self.write_next_token()     # '('
        self.compile_expression()    # expression
        self.write_next_token()     # ')'
        self.write_next_token()     # '{'
        self.compile_statements()    # statements
        self.write_next_token()     # '}'

        if self.peek_next() == "else":
            self.write_next_token()     # 'else'
            self.write_next_token()     # '{'
            self.compile_statements()    # statements
            self.write_next_token()     # '}'


    @tagger(tag="whileStatement")
    def compile_while(self):
        """
        语法："while" "(" expr ")" "{" statements "}"
        父节点： statements
        子节点： expr / statements
        起始： while
        终止："}"
        """
        self.write_next_token()     # 'while'
        self.write_next_token()     # '('
        self.compile_expression()
        self.write_next_token()     # ')'
        self.write_next_token()     # '{'
        self.compile_statements()    # statements
        self.write_next_token()     # '}'


    @tagger(tag="doStatement")
    def compile_do(self):
        """
        语法："do" subroutineCall ";"
        父节点： statements
        子节点： expr  / exprList (subroutineCall不属于子节点，属于类型定义)
        起始： do
        终止：";"
        """
        self.write_next_token() #do
        self.subroutine_call()
        self.write_next_token() # ;

    def subroutine_call(self):
        """
        subroutineName '(' expressionList ')' | ( className | varName) '.' subroutineName '(' expressionList ')'
        不是子节点，不需要加tag
        """
        
        self.write_next_token() # subroutineName or ( className | varName)
        if self.peek_next() == "(":
            self.write_next_token() # "("
            self.compile_expression_list()
            self.write_next_token() # ")"
        elif self.peek_next() == ".":
            self.write_next_token() # "."
            self.write_next_token() # "subroutineName"
            self.write_next_token() # "("
            self.compile_expression_list()
            self.write_next_token() # ")"


    @tagger(tag="returnStatement")
    def compile_return(self):
        """
        语法："return" expr? ";"
        父节点： statements
        子节点： expr
        起始： return
        终止：";"
        """

        self.write_next_token() # return
        if self.peek_next() != ";":
            self.compile_expression()
        self.write_next_token() # ;


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
        self.compile_term()
        while self.peek_next() in OPERATORS:
            self.write_next_token()
            self.compile_term()

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

        if self.peek_next() != ")":
            self.compile_expression()
        
        while self.peek_next() != ")":
            self.write_next_token()
            self.compile_expression()
    
    @tagger(tag="term")
    def compile_term(self):
        """
        integerConstant | stringConstant | keywordConstant | varName | 
        varName '[' expression']' | 
        subroutineCall: subroutineName '(' expressionList ')' | ( className | varName) '.' subroutineName '(' expressionList ')'
        '(' expression ')' | 
        unaryOp term 
        """
        
        if self.peek_next() in UNARY_OPERATORS:  #unaryOp term 
            self.write_next_token() # unaryOP
            self.compile_term() # term
        elif self.peek_next() == "(": #'(' expression ')' 
            self.write_next_token() #(
            self.compile_expression() # expr
            self.write_next_token() # )
        else: #identifier 
            self.write_next_token() # integerConstant | stringConstant | keywordConstant | varName | 
            if self.peek_next() == "[": # expr
                self.write_next_token() # "["
                self.compile_expression()  # expr
                self.write_next_token() # "]"
            elif self.peek_next() == "(":
                self.write_next_token() # "("
                self.compile_expression_list()
                self.write_next_token() # ")"
            elif self.peek_next() == ".":
                self.write_next_token() # "."
                self.write_next_token() # "subroutineName"
                self.write_next_token() # "("
                self.compile_expression_list()
                self.write_next_token() # ")"
    

    def write_tag(self,tag):
            self.write("<{tag}>\n".format(tag=tag))

    def write(self,_xml):
        self.xml.write(_xml)
    
    def write_terminal_token(self):
        token = self.current
        if token.type == 'KEYWORD':
            self.write_token(token.name,'keyword')
        elif token.type == 'SYMBOL':
            self.write_token(token.name,'symbol')
        elif token.type == 'INT_CONSTANT':
            self.write_token(str(token.name),'integerConstant')
        elif token.type == 'STRING_CONSTANT':
            self.write_token(token.name,'stringConstant')
        elif token.type == 'IDENTIFIER':
            self.write_token(token.name,'identifier')

    def write_token(self,token,tag):
            token = token.replace('&', '&amp;')
            token = token.replace('<', '&lt;')
            token = token.replace('>', '&gt;')
            
            self.write("<{tag}> {token} </{tag}>\n".format(tag=tag,token=token))

    