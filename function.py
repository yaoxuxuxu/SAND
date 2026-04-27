from environment import TreeEnv
from StoneException import StoneException
import time
class Function:
    def __init__(self,funname="fun",args=[],astTree=None,env=None):
        self.funname=funname
        self.astTree=astTree
        self.args=args
        self.env=env
    def getName(self):
        return self.funname
    def getArgs(self):
        return self.args
    def getASTtree(self):
        return self.astTree
    def getEnv(self):
        return self.env
    def setEnv(self,env):
        self.env=env
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
                       "getTime":self.eval_getTime,
                       "input":self.eval_input,
                       "int":self.eval_int,

                       #"":self.eval_,
                       }
    def eval(self,native_fun):
        if not isinstance(native_fun,NativeFunction):
            raise StoneException("BUG!")
        funname=native_fun.getName()
        args=native_fun.getArgs()
        if funname not in self.fun_list:
            raise StoneException("No such native function!"+funname)
        return self.fun_list[funname](args)
    def eval_print(self,args):
        for i in args:
            print(i,end=" ")
        print("")
    def eval_getTime(self,args):
        return time.time()
    def eval_input(self,args):
        if len(args)>1:
            raise StoneException("input function at most need 1 param")
        elif len(args)==1:
            return input(args)
        else:
            return input()
    def eval_int(self,args):
        if len(args)!=1:
            raise StoneException("int function only need 1 param")
        tmp=args[0]
        try:
            tmp=int(tmp)
            return tmp
        except:
            raise StoneException("failed to turn to int")
            
#test
if __name__ == "__main__":
    nfm=NativeFunctionManager()
    a=nfm.fun_list["print"]
    a(123)

        