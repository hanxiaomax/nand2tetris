class UnknownSegment(Exception):
    def __init__(self,segment):
        self.segment = segment
    def __str__(self):
        return "Unkown segment [{}]".format(self.segment) 


KIND_SEGMENTS_MAP = {
    "FIELD":"this",  # special mapping. field is object members, store in this segment
    "VAR":"local",  # special mapping. var is for local
    "CONST":"constant", 
    "ARG":"argument", 
    "STATIC":"static", 
    "LOCAL":"local",
    "THIS":"this",
    "THAT":"that", 
    "POINTER":"pointer", 
    "TEMP":"temp"
    }


class VMWriter(object):
    def __init__(self,output):
        self.output = open(output,"w")
    
    def write_push(self,kind,index_or_int):
        """_summary_
        Args:
            kind (_type_): 变量作用域类型
            index_or_int (_type_): 如果是内存段，则为变量在该内存段的序号，如果是const，则为一个正数
        """
        if kind not in KIND_SEGMENTS_MAP:
            raise UnknownSegment(kind)
        
        self.write('push {} {}'.format(KIND_SEGMENTS_MAP[kind], index_or_int))
        
        
    def write_pop(self,kind,index_or_int):
        if kind not in KIND_SEGMENTS_MAP:
            raise UnknownSegment(kind)
        
        self.write('pop {} {}'.format(KIND_SEGMENTS_MAP[kind], index_or_int))
    
    def write_arithmetic(self,command):
        """
        only support lower case arithmetic op
        """
        self.write(command.lower() + '')

    def write_label(self,label):
        self.write('label {}'.format(label))
    
    def write_goto(self,label):
        self.write('goto {}'.format(label))

    def write_if(self,label):
        self.write('if-goto {}'.format(label))

    def write_call(self,name,nargs):
        self.write('call {} {}'.format(name, nargs))

    def write_func(self,name,nlocals):
        self.write('function {} {}'.format(name, nlocals))

    def write_return(self):
        self.write('return')

    def write(self,code):
        print("\t"+code)
        self.output.write(code+"\n")

    def close(self):
        self.output.close()
