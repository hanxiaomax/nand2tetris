from collections import OrderedDict

class SymbolTable(object):
    def __init__(self):
        self.table = OrderedDict()
        self.addEntry('SP',0)
        self.addEntry('LCL',1)
        self.addEntry('ARG',2)
        self.addEntry('THIS',3)
        self.addEntry('THAT',4)
        self.addEntry('SCREEN',16384)
        self.addEntry('KBD',24576)
        self.add_register_label()
        # print("SymbolTable init: \n",self.table)

    def add_register_label(self):
        for i in range(16):
            self.addEntry("R"+str(i),i)

    def addEntry(self,symbol,address):
        self.table[symbol] = address 


    def contains(self,symbol):
        return symbol in self.table

    def get_address(self,symbol):
        if self.contains(symbol):
            return self.table.get(symbol)
        
    
