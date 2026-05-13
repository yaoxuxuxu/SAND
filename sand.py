import os
from SAND.parser import Parser
from SAND.interpreter import Interpreter
import argparse
from CodeGen.modelManager import ModelManager
class SandRunner:
    def __init__(self):
        self.getArgsFromConsole()
    def getArgsFromConsole(self):
        console_parser=argparse.ArgumentParser()
        console_parser.add_argument("file")
        console_parser.add_argument("--tokenize", action="store_true")
        console_parser.add_argument("--asttree", action="store_true")
        console_parser.add_argument("--aifix", action="store_true")
        console_parser.add_argument("--return_all", action="store_true",help="Debug return each value of all the statement.")
        self.args=console_parser.parse_args()
    def debug_parser(self):
        if self.args.tokenize:
            tokens=self.parser.lexer.tokens
            for token in tokens:
                print(token)
            exit(0)
        if self.args.asttree:
            self.showASTtree(self.parser)
            exit(0)
        return
        
    @staticmethod
    def read_file(dir):
        try:
            with open(dir,"r+") as fp:
                code=fp.read()
            return code
        except:
            print("No such file!!!")
            return -1
    @staticmethod
    def showASTtree(parser):
        for i in parser.parse():
            print(i)
        return
    def run(self):
        dir=os.path.abspath(self.args.file)
        self.itpt=Interpreter(os.path.dirname(dir))
        for i in self.parser.parse():
            result=self.itpt.eval(i)
            if self.args.return_all:
                print(result)
    def aifix(self,code):
        mm=ModelManager()
        code=mm.fix_code(code)
        while True:
            try:
                Parser(code).parse()
                break
            except Exception as ec:
                print("Error!!! Try to fix!!!")
                code=mm.fix_code(str(ec))

        with open("./temp.sand", "w+") as fp:
            fp.write(code)
        return code
    def main(self):
        #code level
        dir=self.args.file
        code=self.read_file(dir)
        if code==-1:
            return
        if self.args.aifix:
            code=self.aifix(code)

        #parser level
        self.parser=Parser(code)
        self.debug_parser()

        #interpreter level
        self.run()
        
if __name__ == "__main__":
    sr=SandRunner()
    sr.main()

