from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine
import sys

class JackAnalyzer(object):
    def __init__(self,filename):
        tokenizer = JackTokenizer(filename)

    def run(self):
        pass 

if __name__ == "__main__":

    filename = sys.argv[1]
    analyzer  = JackAnalyzer(filename)

