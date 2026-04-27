from asttree import ASTfruit,ASTnode
from StoneException import InterpreterException
from environment import Environment,TreeEnv
from function import Function,NativeFunction,NativeFunctionManager
import time
class Interpreter:
    def __init__(self):
        self.global_env=Environment()
        self.set_native_function()
        self.now_env=self.global_env

    def debug(self):
        print(self.now_env.var)
        print(self.now_env)
        time.sleep(0.1)
    def eval(self,astTree):
        #self.debug()
        if astTree.getType()=="function":
            return self.create_fun(astTree)
        if astTree.getType()=="statement":
            return self.do_state(astTree)
        if astTree.getType()=="expression":
            return self.do_expr(astTree)
        if astTree.getType()=="primary":
            return self.do_pri(astTree)

        last=None
        for i in astTree.child:
            last=self.eval(i)
        return last
    def set_native_function(self):
        self.nfm=NativeFunctionManager()
        for i in self.nfm.fun_list:
            self.global_env.setValue(i,NativeFunction(i,[]))
        
    def create_fun(self,astTree):
        name=astTree.child[0].getValue()
        param=astTree.child[1]
        fun=astTree.child[2]
        args=self.get_args(param)
        return self.env_add_fun(name,args,fun)
    def env_add_fun(self,name,args,astTree):
        return self.now_env.setValue(name,Function(name,args,astTree,self.now_env)) 
    def do_state(self,astTree):
        if type(astTree) is ASTfruit:
            op=astTree.getValue()
            if op=="if":
                return self.do_if_block(astTree)
            if op=="while":
                return self.do_while_block(astTree)
            raise InterpreterException("Bad Statement!",astTree.getToken())
        return self.eval(astTree.child[0])
    def do_if_block(self,astTree):
        num_state=len(astTree.child)
        if num_state<=1 or num_state>3:
            raise InterpreterException("Bad if block!",astTree.getToken())
        if self.eval(astTree.child[0]):
            return self.eval(astTree.child[1])
        elif num_state>=3:
            return self.eval(astTree.child[2])
    def do_while_block(self,astTree):
        num_state=len(astTree.child)
        if num_state!=2:
            raise InterpreterException("Bad while block!",astTree.getToken())
        tmp=0
        while self.eval(astTree.child[0]):
            tmp=self.eval(astTree.child[1])
        return tmp
    def do_expr(self,astTree):
        if type(astTree) is ASTfruit and len(astTree.child)==2:
            op=astTree.getValue()
            left=astTree.child[0]
            right=astTree.child[1]
            if op=="+":
                return self.eval(left)+self.eval(right)
            if op=="-":
                return self.eval(left)-self.eval(right)
            if op=="*":
                return self.eval(left)*self.eval(right)
            if op==">":
                return self.eval(left)>self.eval(right)
            if op=="<":
                return self.eval(left)<self.eval(right)
            if op==">=":
                return self.eval(left)>=self.eval(right)
            if op=="<=":
                return self.eval(left)<=self.eval(right)
            if op=="/":
                right=self.eval(right)
                self.isDivideZero(right,astTree)
                return self.eval(left)/right
            if op=="%":
                right=self.eval(right)
                self.isDivideZero(right,astTree)
                return self.eval(left)%right
            if op=="=":
                var=self.getVarNameFromAsttree(left)
                if var:
                    return self.now_env.setValue(var,self.eval(right))
                else:
                    raise InterpreterException("failed to set value of",left.getToken())

        return self.eval(astTree.child[0])
    def getVarNameFromAsttree(self,astTree):
        if type(astTree)==ASTfruit:
            token=astTree.getToken()
            if token.getType()=="IDENTIFIER":
                return token.getValue()
        return 0
    def do_pri(self,astTree):
        if len(astTree.child)==0 and type(astTree)==ASTfruit:
            varname=self.getVarNameFromAsttree(astTree)
            if varname:
                return self.now_env.getValue(varname)
            return astTree.getValue()
        elif len(astTree.getChild())>0 and astTree.getChild(0).getType()=="postfix":
            return self.do_postfix(astTree)
        elif astTree.getValue()=="lambda":
            return self.do_lambda(astTree)
        return self.eval(astTree.child[0])
    def do_lambda(self,astTree):
        args=self.get_args(astTree.child[0])
        fun=astTree.child[1]
        return Function("lambda",args,fun,self.now_env)
    def do_postfix(self,primary):
        if primary.getToken().getType()!="IDENTIFIER":
            raise InterpreterException("Bad Function",primary.getToken())
        fun_name=primary.getValue()
        child=primary.getChild()
        for postfix in child:
            if postfix.getType() != "postfix":
                raise InterpreterException("Bad postfix")
            fun_name=self.do_fun(fun_name,self.get_args(postfix))
        return fun_name
    def init_env(self,fun,args):
        funargs=fun.getArgs()
        self.now_env=TreeEnv(fun.getEnv())
        fun.setEnv(self.now_env)
        astTree=fun.getASTtree()
        if len(funargs)!=len(args):
            raise InterpreterException("args not match"+fun.getName())
        for i in range(len(funargs)):
            #print("set",funargs[i],args[i])
            self.now_env.setValueForce(funargs[i],args[i])
            #print(env.var)
        return astTree
    def do_fun(self,name,args):
        fun=self.now_env.getValue(name)
        if isinstance(fun,NativeFunction):
            fun.setArgs(args)
            return self.nfm.eval(fun)
        #in
        astTree=self.init_env(fun,args)
        #do
        result=self.eval(astTree)
        #out
        self.now_env=fun.getEnv()
        self.now_env=self.now_env.getFatherEnv()
        fun.setEnv(self.now_env)
        
        if self.now_env==None:
            raise InterpreterException("Environment error!Now env is None")
        return result
    def isDivideZero(self,value,astTree):
        if value==0:
            raise InterpreterException("Divide Zero!\n",astTree.getToken())
        return
    def get_args(self,astTree):
        if astTree.getType()=="postfix":
            astTree=astTree.getChild(0)
        if astTree.getType()=="param_list":
            if not astTree.hasChild():
                return []
            astTree=astTree.getChild(0)
        args=[]
        if astTree.getType()=="params":
            for i in astTree.getChild():
                args.append(i.getValue())
        if astTree.getType()=="args":
            for i in astTree.getChild():
                args.append(self.eval(i))
        
        return args
if __name__ == "__main__":
    itpt=Interpreter()