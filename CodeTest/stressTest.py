from . import utils
from .test_template import one_function_testcode
import json
import os
class StressTester:
    def __init__(self,code,std,datagen):
        self.testcode=code
        self.std=std
        self.module=utils.loadModuleFromPythonFile(datagen)
        self.data=self.module.generate()
    def set_files(self):
        with open("CodeTest/temp/testcode.py","w+",encoding="utf-8") as fp:
            fp.write(self.testcode)
        with open("CodeTest/temp/stdcode.py","w+",encoding="utf-8") as fp:
            fp.write(self.std)
    def test_once(self,param):
        pre_dir=os.getcwd()
        os.chdir("CodeTest/temp/")
        param=json.dumps(param)[1:-1]
        if hasattr(self.module,"test"):
            code=self.module.test(param)
        else:
            code=one_function_testcode(param)
        #print(code)
        env={}
        exec(code,env)
        os.chdir(pre_dir)
        if env['result']:
            return "Accepted"
        else:
            return "Wrong Answer"
    def test(self):
        case=1
        self.set_files()
        for param in self.data:
            print(f"Test case: {str(case)}")
            result=self.test_once(param)
            if result!="Accepted":
                print("Wrong Answer")
                return result
            else:
                print("Accecpted")
            case+=1
        return "Accepted"

if __name__ == "__main__":
    for i in range(1,10+1):
        with open(f"./CodeTest/one_function/std{i}.py","r+") as fp:
            code=fp.read()
        st=StressTester(code,code,f"./CodeTest/one_function/data{i}.py").test()