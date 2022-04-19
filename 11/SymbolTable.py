from cgitb import reset
from collections import OrderedDict
import json
class UndefinedVarException(Exception):
    def __init__(self,name):
        self.name = name
    def __str__(self):
        return "Undefined variable name [{}]".format(self.name) 
class UnsupportedVarKind(Exception):
    def __init__(self,kind):
        self.kind = kind
    def __str__(self):
        return "Unsupported variable kind [{}]".format(self.kind) 

class Symbol(object):
    def __init__(self,_name,_type,_kind,_index):
        self._name = _name
        self.symbol = {
            "type":_type,
            "kind":_kind,
            "index":_index,
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
    """符号表
    支持任意级嵌套的作用域，对于本项目只需要两级（class level 和 subroutine level）
    支持输出符号表结构到 json 文件
    默认符号表包含两个:
    - static 为文件作用域，在 compile_jackfile 中创建
    - class 为类作用域，在compile_class中创建
    """
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
        
    

    def create_table(self,name,_type):
        """
        在链表尾部插入一个新的表，没进入一个新的作用域时调用一次，退出作用域时进行删除
        默认的两个表在0,1位置，分别为全局作用域和类作用域
        """
        table = {
            "name" : name, 
            "type" : _type,
            "entry" : OrderedDict()
        }
        self.symbol_tables.append(table)
        #只需要创建表的时候将其加入即可，这里是引用，对表的操作是同步的
        self.json_output.append(table) 

    def start_subroutine(self,name,class_name):
        """创建subroutine level 符号表
        Args:
            name (str): 当前符号表名 
            class_name (str): 当前符号表所属类的类名，用于确定this变量的类别
        总是包含一个this变量
        """
        self.count["VAR"] = 0
        self.count["ARG"] = 0
        self.create_table(name,"Subroutine")
        # 默认的第一个参数

    def end_subroutine(self):
        """
        退出 subroutine 时调用，用于清理当前 subroutine level的符号表
        """
        del self.symbol_tables[-1] 

    def subroutine_scope_table(self):
        return self.symbol_tables[-1]
    
    def global_scope_table(self):
        """
        返回static符号表，即文件作用域
        """
        return self.symbol_tables[0]
    
    def class_scope_table(self):
        """
        返回 class 符号表，即 field
        """
        return self.symbol_tables[1]

    def define(self,name,_type,kind):
        kind = kind.upper()
        if kind == "STATIC":
            table = self.global_scope_table()
        elif kind == "FIELD":
            table = self.class_scope_table()
        elif kind == "VAR" or kind == "ARG":
            table = self.subroutine_scope_table()
        else:
            raise UnsupportedVarKind(kind)
        
        symbol = Symbol(name,_type,kind,self.count[kind])
        table["entry"][name] = symbol
        self.count[kind]+=1

    def search_symbol(self,name):
        for table in self.symbol_tables[::-1]: #从链表尾部向前遍历，尾部为最新的作用域
            if name in table["entry"].keys():
                return table["entry"][name]
        
        return None

    def dump(self):
        """
        将符号表输出到json文件中。
        注意，如果程序没有正确执行，输出的符号表也是不完整的。
        """
        with open(self.symbol_file,"w") as f:
            json.dump(self.json_output, f ,indent=4,default=self.tojson)
        
        return self.symbol_file

    def tojson(self,obj):
        """
        自定义的序列化函数，针对不同类型的对象，调用其各自的序列化函数
        """
        if isinstance(obj,Symbol):
            return obj.tojson()

    ### API START####
    def var_count(self,kind):
        return self.count.get(kind)

    def kindof(self,name):
        result = self.search_symbol(name)
        return result.kind if result else None

    def typeof(self,name):
        result = self.search_symbol(name)
        return result.type if result else None

    def indexof(self,name):
        result = self.search_symbol(name)
        return result.index if result else None

    ### API END####

