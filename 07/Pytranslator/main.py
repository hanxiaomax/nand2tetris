import sys
from Translator import Translator
if __name__ == "__main__":
    # vmfile = "MemoryAccess/BasicTest/BasicTest.vm"
    vmfile = sys.argv[1]
    with Translator (vmfile) as translator:
        translator.run()
    
## 测试需要使用 CPU Emulator，加载生成的asm文件以及.tst测试文件(文件名中不包括VM)