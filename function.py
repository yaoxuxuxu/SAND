from environment import IndexEnv
from StoneException import FunctionException
from asttree import ASTnode,ASTfruit,ASTvar
import time
class Function:
    def __init__(self,funname="fun",args=[],astTree=None,env=None,varSize:int=0):
        self.funname=funname
        self.astTree=astTree
        self.args=args
        self.varsize=0
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
        self.env=IndexEnv(self.env)
        if len(self.args) != len(args):
            raise FunctionException("The number of the arguments is not correct")
        for i in range(len(args)):
            self.env.setValue(self.args[i],args[i])
        return self.env
    def runUnwind(self):
        self.env=self.env.getFatherEnv()
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
                       "getTime":self.eval_getTime,
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
    def eval_getTime(self,args):
        return time.time()
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
            tmp=int(tmp)
            return tmp
        except:
            raise FunctionException("failed to turn to int")

class FunctionVarOptimizer:
    def __init__(self):
        self.index=0
        self.depth=1
        self.local_var={}
    def isVar(self,astTree):
        if astTree.getChildNum()==0 and astTree.getType()=="primary":
            token=astTree.getToken()
            if token!=None and token.getType()=="IDENTIFIER":
                return True
        return False
    def getVar(self,varname):
        if varname in self.local_var:
           return self.local_var[varname]
        else:
            pos=(self.depth,self.index)
            self.index+=1
            self.local_var[varname]=pos
            return pos
             
    def replace_var(self,astTree):
        depth,index=self.getVar(astTree.getValue())
        newnode=ASTvar.transferFromASTfruit(astTree,depth,index)
        self.index+=1
        return newnode
    def find_var(self,astTree):
        #find child
        child=astTree.getChild()
        for i in range(len(child)):
            if self.isVar(child[i]):
                child[i]=self.replace_var(child[i])
            self.find_var(child[i])
    def optimize(self,fun:Function):
        astTree=fun.getASTtree()
        self.find_var(astTree)
    

#test
if __name__ == "__main__":
    nfm=NativeFunctionManager()
    a=nfm.fun_list["print"]
    a(123)

        