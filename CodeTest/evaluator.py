from SAND.parser import Parser
from SAND.interpreter import Interpreter

class SandEvaluator:
    def __init__(self, code):
        self.code=code
    def check_all(self,**args):
        status,message=self.syntax_check()
        if not status:
            return "Syntax_Error",message
        status,message=self.runtime_check()
        if not status:
            return "Runtime_Error",message
        status,message=self.performance_check(**args) 
        if not status:
            return "Performance_Error",message
        return "pass","complete"
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
        match mode:
            case "std":
                pass
            case "data":
                return self.checkByData(args["tests"],args["funname"])
    @staticmethod
    def toSandVar(x):
        res=x
        match res:
            case str():
                res=res.replace("True","true")
                res=res.replace("False","false")
                res=res.replace("'",'"')
        return res
                
        
    def checkByData(self,test_cases,funname):
        case_id=0
        try:
            for testcase in test_cases:
                print(f"Testing Case {case_id}:")
                input_data=self.toSandVar(testcase["input"])
                output_data=self.toSandVar(testcase["output"])
                testcode=self.code+f"\n\n{funname}({input_data})=={output_data}"
                print(testcode)
                self.itpt=Interpreter("./CodeTest/temp/")
                for i in Parser(testcode).parse():
                    result=self.itpt.eval(i)
                if result:
                    print("Accepted")
                else:
                    print("Wrong answer")
                    return False,testcase
                case_id+=1
            return True,"pass"
        except Exception as e:
            return False,str(e)    

    
