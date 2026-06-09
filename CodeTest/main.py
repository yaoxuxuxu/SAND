from SAND.parser import Parser
from SAND.interpreter import Interpreter
import os

class Tester:
    def __init__(self):
        pass
    def run_test(self,file):
        with open(file,"r+",encoding="utf-8") as fp:
            fp.read()
        try:
            code=Parser(file).parse()
        except Exception as e:
            raise Exception("Syntax Error\n"+str(e))
        try:
            self.itpt=Interpreter(os.path.dirname(file))
            for i in self.parser.parse():
                result=self.itpt.eval(i)
        except Exception as e:
            raise Exception("Runtime Error\n"+str(e))
        
if __name__ == "__main__":
    test=Tester()
    test.run_test("")