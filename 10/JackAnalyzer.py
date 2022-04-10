from lib2to3.pgen2.tokenize import tokenize
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine
import sys
import os

class JackAnalyzer(object):
    def __init__(self,basedir):
        self.jackfiles = self.collect_files(basedir)
    
    def collect_files(self,path):
        return [ os.path.join(path,file) for file in os.listdir(path) if file.endswith(".jack")]

    def generate_type_xml(self,jackfile):
        with CompilationEngine(jackfile) as ce:
            tokenizer = JackTokenizer(jackfile)
            tokens = []
            ce.write('<tokens>\n')
            while tokenizer.has_more_tokens():
                token = tokenizer.advance()
                tokens.append((token,tokenizer.token_type()))
                if tokenizer.token_type() == 'KEYWORD':
                    ce.write_token('keyword', token)
                elif tokenizer.token_type() == 'SYMBOL':
                    ce.write_token('symbol', token)
                elif tokenizer.token_type() == 'INT_CONSTANT':
                    ce.write_token('integerConstant', str(token))
                elif tokenizer.token_type() == 'STRING_CONSTANT':
                    ce.write_token('stringConstant', token)
                elif tokenizer.token_type() == 'IDENTIFIER':
                    ce.write_token('identifier', token)
            ce.write('</tokens>')
            for token in tokens:
                print("{: <25}:  {: <30}".format(token[0],token[1]))

    def generate_xml(self,jackfile):
        with CompilationEngine(jackfile) as ce:
            tokenizer = JackTokenizer(jackfile)
            ce.set_tokenizer(tokenizer)
            ce.compile_class() # 总是从Class Main开始

    def run(self):
        for jackfile in self.jackfiles:
            print("="*40 + "\n" + jackfile +"\n" +"="*40)
            self.generate_type_xml(jackfile)
            

if __name__ == "__main__":

    # basedir = "/Users/lingfengai/code/nand2tetris/projects/10/ArrayTest"#sys.argv[1]
    basedir = sys.argv[1]
    analyzer  = JackAnalyzer(basedir)
    analyzer.run()
    
