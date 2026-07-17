from SAND.parser import Parser
from SAND.interpreter import Interpreter

class Evaluator:
    def __init__(self, code):
        self.code=code
    def syntax_check(self):
        try:
            Parser(self.code).parse()
            return True,"pass"
        except Exception as e:
            return False,str(e)
    def runtime_check(self):
        try:
            self.itpt=Interpreter("./CodeTest/temp/")
            for i in Parser(self.code).parse():
                result=self.itpt.eval(i)
            return True,"pass"
        except Exception as e:
            return False,str(e)
    def performance_check(self,mode:str,**args):
        if mode=="time":
            import time
            start=time.time()
            for i in Parser(self.code).parse():
                result=self.itpt.eval(i)
            end=time.time()
            return True,end-start
        elif mode=="memory":
            import tracemalloc
            tracemalloc.start()
            for i in Parser(self.code).parse():
                result=self.itpt.eval(i)
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            return True,peak

    
