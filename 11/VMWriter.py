class UnknownSegment(Exception):
    def __init__(self,segment):
        self.segment = segment
    def __str__(self):
        return "Unkown segment [{}]".format(self.segment) 


SEGMENTS_MAP = {
    "CONST":"constant", 
    "ARG":"argument", 
    "VAR":"local",  # var is for local
    "STATIC":"static", 
    "THIS":"this", 
    "THAT":"that", 
    "POINTER":"pointer", 
    "TEMP":"temp"
    }


class VMWriter(object):
    def __init__(self,output):
        self.output = open(output,"w")
    
    def write_push(self,segment,index):
        if segment not in SEGMENTS_MAP:
            raise UnknownSegment(segment)
        
        self.write('push {} {}'.format(SEGMENTS_MAP[segment], index))
        
    def write_pop(self,segment,index):
        if segment not in SEGMENTS_MAP:
            raise UnknownSegment(segment)
        
        self.write('pop {} {}'.format(SEGMENTS_MAP[segment], index))
    
    def write_arithmetic(self,command):
        self.write(command + '')

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
        self.output.write(code+"\n")

    def close(self):
        self.output.close()
