class VMWriter(object):
    def __init__(self,output):
        self.output = open(output,"w")
    
    def write_push(self,segment,index):
        pass

    def write_pop(self,segment,index):
        pass
    
    def write_arithmetic(self,command):
        pass

    def write_label(self,lable):
        pass
    
    def write_goto(self,lable):
        pass

    def write_if(self,lable):
        pass

    def write_call(self,name,nargs):
        pass

    def write_func(self,name,nlocals):
        pass

    def write_return(self):
        pass

    def close(self):
        self.output.close()