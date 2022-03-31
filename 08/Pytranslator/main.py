import sys
import os
from Translator import Translator
from CodeWriter import CodeWriter

###
# 目录下所有的vm文件都要处理并生成一个以目录命名的asm文件，但是处理的顺序没有关系
###
def collect_files(path):
    return [ os.path.join(path,file) for file in os.listdir(path) if file.endswith(".vm")]

def call_bootstrap(vmfiles):
    for vmfile in vmfiles:
        vmfilename = vmfile.split("/")[-1]
        if vmfilename == "Sys.vm":
            print("\nFind Sys.vm, Bootstrap code called .......")
            code_writer.write_init()


if __name__ == "__main__":
    basedir = sys.argv[1]
    vmfiles = collect_files(basedir)
    asmfile = os.path.join(basedir,basedir.split("/")[-1]) + ".asm"
    print("Input vm files: ",vmfiles)
    print("Target file: ",asmfile)

    with CodeWriter(asmfile) as code_writer:
        call_bootstrap(vmfiles)
        for vmfile in vmfiles:
            translator = Translator(vmfile)
            vmfilename = vmfile.split("/")[-1].split(".")[0]
            code_writer.set_filename_namespace(vmfilename)
            translator.set_codewriter(code_writer)
            translator.translate()
            translator.close()

## 测试需要使用 CPU Emulator，加载生成的asm文件以及.tst测试文件(文件名中不包括VM)