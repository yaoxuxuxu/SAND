from SAND.parser import Parser
from SAND.interpreter import Interpreter
import os
import CodeTest.utils as utils
from CodeGen import fewshot,formatParser

class Tester:
    def __init__(self,test_dir):
        self.tests=self.getTests(test_dir)
    def getTests(self,test_dir):
        prompts=[]
        stds=[]
        for dir in os.listdir(test_dir):
            if "prompt" in dir:
                prompts.append(dir)
            if "std" in dir:
                stds.append(dir)
        prompts.sort(key=utils.getNumberFromStr)
        stds.sort(key=utils.getNumberFromStr)
        formatParser.Parser()
        tests=[]
        for i in range(len(prompts)):
            prompt=os.path.join(test_dir,prompts[i])
            std=os.path.join(test_dir,stds[i])
            with open(prompt,"r+") as fp:
                prompt=fp.read()
            with open(std,"r+") as fp:
                std=fp.read()

            tests.append({"prompt":prompt,"std":std})
        return tests
    def test_once(self,test,model):
        model=model()
        model.user_add(test['prompt'])
        code=model.send("complete the code")
        code=formatParser.Parser().parse("stone",code)
        with open("./CodeTest/generate.txt","w+") as fp:
            fp.write(code)
        
        self.run_test(code)
        
    def run_test(self,code):
        try:
            code=Parser(code).parse()
        except Exception as e:
            raise Exception("Syntax Error\n"+str(e))
        try:
            self.itpt=Interpreter("CodeTest/")
            for i in self.parser.parse():
                result=self.itpt.eval(i)
        except Exception as e:
            raise Exception("Runtime Error\n"+str(e))
        
if __name__ == "__main__":
    test=Tester("CodeTest/one_function")
    test.test_once(test.tests[0],fewshot.baseline)