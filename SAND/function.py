from .environment import TreeEnv
from .StoneException import FunctionException
import time
class Function:
    def __init__(self,funname="fun",args=[],astTree=None,env=None):
        self.funname=funname
        self.astTree=astTree
        self.args=args
        self.env=env
    def getName(self):
        return self.funname
    def copy(self):
        return Function(self.funname,self.args,self.astTree,self.env)
    def getArgs(self):
        return self.args
    def getASTtree(self):
        return self.astTree
    def getEnv(self):
        return self.env
    def setEnv(self,env):
        self.env=env
    def runInit(self,args):
        frame=TreeEnv(self.env)
        if len(self.args) != len(args):
            raise FunctionException("The number of the arguments is not correct")
        for i in range(len(args)):
            frame.setValueForce(self.args[i],args[i])
        return frame
    def runUnwind(self):
        return self.env
class NativeFunction:
    def __init__(self,funname="",args=[]):
        self.name=funname
        self.args=args
    def getName(self):
        return self.name
    def getArgs(self):
        return self.args
    def setArgs(self,args):
        self.args=args
        
class NativeFunctionManager:    
    def __init__(self):
        self.fun_list={"print":self.eval_print,
                       "input":self.eval_input,
                       "int":self.eval_int,
                       "str":self.eval_str,
                       #"":self.eval_,
                       }
    def eval(self,native_fun):
        if not isinstance(native_fun,NativeFunction):
            raise FunctionException("BUG!")
        funname=native_fun.getName()
        args=native_fun.getArgs()
        if funname not in self.fun_list:
            raise FunctionException("No such native function!"+funname)
        return self.fun_list[funname](args)
    def eval_str(self,args):
        if len(args)>1:
            raise FunctionException("str function at most need 1 param")
        return str(args[0])
    def eval_print(self,args):
        for i in args:
            print(i,end=" ")
        print("")
    def eval_input(self,args):
        if len(args)>1:
            raise FunctionException("input function at most need 1 param")
        elif len(args)==1:
            return input(args)
        else:
            return input()
    def eval_int(self,args):
        if len(args)!=1:
            raise FunctionException("int function only need 1 param")
        tmp=args[0]
        try:
            tmp=float(tmp)
            tmp=int(tmp)
            return tmp
        except:
            raise FunctionException("failed to turn to int")
            
#test
if __name__ == "__main__":
    nfm=NativeFunctionManager()
    a=nfm.fun_list["print"]
    a(123)

        