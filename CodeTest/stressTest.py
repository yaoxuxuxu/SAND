from . import utils
from .test_template import one_function_testcode
from SAND.parser import Parser
from SAND.interpreter import Interpreter
class StressTester:
    def __init__(self,code,std,datagen):
        self.testcode=code
        self.std=std
        self.data=self.data_generate(datagen)
    def data_generate(self,datagen):
        module=utils.loadModuleFromPythonFile(datagen)
        return module.generate()
    def set_files(self):
        with open("./CodeTest/temp/testcode.sand","w+",encoding="utf-8") as fp:
            fp.write(self.testcode)
        with open("./CodeTest/temp/stdcode.sand","w+",encoding="utf-8") as fp:
            fp.write(self.std)
    def test_once(self,param):
        code=one_function_testcode(*param)
        itpt=Interpreter("./CodeTest/temp/")
        for i in Parser(code).parse():
            result=itpt.eval(i)
        if result:
            pass
        else:
            return "Wrong Answer"
        return "Accepted"

    def test(self):
        self.set_files()
        for param in self.data:
            result=self.test_once(param)
            if result!="Accepted":
                return result
        return "Accepted"

if __name__ == "__main__":
    with open("./CodeTest/one_function/std1.txt","r+") as fp:
        code=fp.read()
    st=StressTester(code,code,"./CodeTest/one_function/data1.py").test()