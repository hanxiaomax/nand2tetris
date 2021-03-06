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
            ce.set_tokens(tokenizer.get_tokens())
            ce.write_tag("tokens")
            while ce.has_more_tokens():
                ce.write_next_token()
            ce.write_tag("/tokens")
                
    def generate_xml(self,jackfile):
        with CompilationEngine(jackfile) as ce:
            tokenizer = JackTokenizer(jackfile)
            ce.set_tokens(tokenizer.get_tokens())
            # ce.print_tokens()
            ce.compile_jackfile() # 总是从Class Main开始
            

    def run(self):
        for jackfile in self.jackfiles:
            print("="*40 + "\n" + jackfile +"\n" +"="*40)
            # self.generate_type_xml(jackfile)
            self.generate_xml(jackfile)

if __name__ == "__main__":

    #basedir = "/Users/lingfengai/code/nand2tetris/projects/11/ConvertToBin/"#sys.argv[1]
    basedir = sys.argv[1]
    analyzer  = JackAnalyzer(basedir)
    analyzer.run()
    
