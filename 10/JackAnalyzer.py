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
        with CompilationEngine(jackfile,"TXML") as ce:
            tokenizer = JackTokenizer(jackfile)
            ce.write('<tokens>\n')
            while tokenizer.has_more_tokens():
                ce.curr_token,ce.token_type = tokenizer.advance()
                print("{: <25}:  {: <30}".format(str(ce.curr_token),str(ce.token_type)))
                ce.write_terminal_token()
            ce.write('</tokens>')
                
    def generate_xml(self,jackfile):
        with CompilationEngine(jackfile) as ce:
            tokenizer = JackTokenizer(jackfile)
            ce.set_tokenizer(tokenizer)
            ce.compile_class() # 总是从Class Main开始

    def run(self):
        for jackfile in self.jackfiles:
            print("="*40 + "\n" + jackfile +"\n" +"="*40)
            self.generate_type_xml(jackfile)
            self.generate_xml(jackfile)

if __name__ == "__main__":

    basedir = "/Users/lingfengai/code/nand2tetris/projects/10/ArrayTest"#sys.argv[1]
    #basedir = sys.argv[1]
    analyzer  = JackAnalyzer(basedir)
    analyzer.run()
    
