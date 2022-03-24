JUMP_TABLE = {
    "JGT": '001',
    "JEQ": '010',
    "JGE": '011',
    "JLT": '100',
    "JNE": '101',
    "JLE": '110',
    "JMP": '111',
}
C_CMD_TABLE = {
    '0': '0101010',
    '1': '0111111',
    '-1': '0111010',
    'D': '0001100',
    'A': '0110000',
    'M': '1110000',
    '!D': '0001101',
    '!A': '0110001',
    '!M': '1110001',
    '-D': '0001111',
    '-A': '0110011',
    '-M': '1110011',
    'D+1': '0011111',
    'A+1': '0110111',
    'M+1': '1110111',
    'D-1': '0001110',
    'A-1': '0110010',
    'M-1': '1110010',
    'D+A': '0000010',
    'D+M': '1000010',
    'D-A': '0010011',
    'D-M': '1010011',
    'A-D': '0000111',
    'M-D': '1000111',
    'D&A': '0000000',
    'D&M': '1000000',
    'D|A': '0010101',
    'D|M': '1010101',
}
DEST_TABLE = {
    "M" : '001',
    "D" : '010',
    "MD":'011',
    "A":'100',
    "AM":'101',
    "AD":'110',
    "AMD":'111'
}
class Code(object):
    @staticmethod
    def dest(d):
            return DEST_TABLE.get(d,'000')

    @staticmethod
    def comp(c):
            return C_CMD_TABLE.get(c,'0000000')
        
    @staticmethod
    def jump(j):
        if j:
            j = j[1:]
            return JUMP_TABLE.get(j,'000')
        else:
            return "{0:03b}".format(0)

    @staticmethod
    def address(var):
        return "{0:016b}".format(int(var))