import traceback

class CompilationEngine(object):
    def __init__(self,jackfile):
        self.xmlfile = jackfile.replace(".jack","T-my.xml")
        self.indent = 0
        

    def __enter__(self):
        print("Open file ",self.xmlfile)
        self.xml = open(self.xmlfile,'w')
        self.write('<tokens>\n')
        # self.change_indent(2)
        return self

    def __exit__(self,exc_type,exc_val,exc_tb):
        # self.change_indent(-2)
        self.write('</tokens>\n')
        self.xml.close()
        print("CompilationEngine exit, close ",self.xmlfile)
        if exc_val:
            print("exit:", exc_type, exc_val, exc_tb)
            print(traceback.print_tb(exc_tb))
        return True

    def write_token(self,token_type,token):
        token = token.replace('&', '&amp;')
        token = token.replace('<', '&lt;')
        token = token.replace('>', '&gt;')

        self.write(' ' * self.indent + '<' + token_type + '> ')
        self.write(token)
        self.write(' </' + token_type + '>\n')
    
    def write(self,_xml):
        self.xml.write(_xml)

    def change_indent(self,val):
        self.indent += val

    def compile_class(self):
    
        pass

    def compile_class_var_dec(self):
        pass

    def compile_subroutine(self):
        pass

    def compile_parameter_list(self):
        pass

    def compile_var_dec(self):
        pass

    def compile_statements(self):
        pass

    def compile_do(self):
        pass

    def compile_let(self):
        pass

    def compile_while(self):
        pass

    def compile_return(self):
        pass

    def compile_if(self):
        pass

    def compile_expression(self):
        pass

    def compile_term(self):
        pass

    def compile_expression_list(self):
        pass