from collections import OrderedDict
import json
class UndefinedVarException(Exception):
    def __str__(self,name):
        return "Undefined variable name {}".format(name) 

class Symbol(object):
    def __init__(self,_name,_type,_kind,_index):
        self._name = _name
        self.symbol = {
            "type":_type,
            "kind":_kind,
            "index":_index
        }

    def __str__(self):
        return "{: <20}{: <20}{: <20}{: <20}".format(self._name,self._type,self._kind,str(self.index))

    @property
    def kind(self):
        return self.symbol["kind"]

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self.symbol["type"]
    
    @property
    def index(self):
        return self.symbol["index"]
    
    def tojson(self):
        return self.symbol



class SymbolTable(object):
    def __init__(self,symbol_file):
        self.count = {
            "STATIC":0,
            "FIELD":0,
            "VAR":0,
            "ARG":0
        }
        self.symbol_tables = []
        self.json_output = [] # 用于输出json格式的符号表，subroutine的所有表都包含在内
        self.symbol_file =symbol_file
        # 创建默认的符号表
        self.create_table("global")# 全局作用域 static 符号表
        self.create_table("class")# 类作用域 field 符号表

    def create_table(self,name):
        """
        在链表尾部插入一个新的表，没进入一个新的作用域时调用一次，退出作用域时进行删除
        默认的两个表在0,1位置，分别为全局作用域和类作用域
        """
        table = {
            "name" : name,
            "entry" : OrderedDict()
        }
        self.symbol_tables.append(table)
        #只需要创建表的时候将其加入即可，这里是引用，对表的操作是同步的
        self.json_output.append(table) 

    def start_subroutine(self,name,class_name):
        # reset counter
        self.count["VAR"] = 0
        self.count["ARG"] = 0
        self.create_table("Subroutine:"+name)
        # 默认的第一个参数
        self.define("this",class_name,"ARG")

    def end_subroutine(self):
        del self.symbol_tables[-1] #方便打印，不直接删除而是修改index

    def subroutine_scope_table(self):
        return self.symbol_tables[-1]
    
    def global_scope_table(self):
        return self.symbol_tables[0]
    
    def class_scope_table(self):
        return self.symbol_tables[1]

    def define(self,name,_type,kind):
        if kind == "STATIC":
            table = self.global_scope_table()
        elif kind == "FIELD":
            table = self.class_scope_table()
        elif kind == "VAR" or kind == "ARG":
            table = self.subroutine_scope_table()
        else:
            raise
        
        symbol = Symbol(name,_type,kind,self.count[kind])
        table["entry"][name] = symbol
        self.count[kind]+=1

    def var_count(self,kind):
        return self.count[kind]

    def search_symbol(self,name):
        for table in self.symbol_tables[::-1]: #从链表尾部向前遍历，尾部为最新的作用域
            if name in table["entry"].keys():
                return table.get(name)
        
        raise UndefinedVarException(name)
                
    def kindof(self,name):
        return self.search_symbol(name).kind

    def typeof(self,name):
        return self.search_symbol(name).type

    def indexof(self,name):
        return self.search_symbol(name).index

    def dump(self):
        with open(self.symbol_file,"w") as f:
            json.dump(self.json_output, f ,indent=4,default=self.tojson)

    def tojson(self,obj):
        return obj.tojson()