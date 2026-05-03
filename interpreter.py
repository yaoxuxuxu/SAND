from asttree import ASTfruit,ASTnode
from StoneException import InterpreterException
from environment import Environment,TreeEnv
from function import Function,NativeFunction,NativeFunctionManager
from oop import Class,ClassInstance
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
        if astTree.getType()=="class":
            return self.create_class(astTree)
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
    def create_class(self,astTree):
        child=astTree.getChild()
        if len(child)==2:
            classname=self.getVarNameFromAsttree(child[0])
            astTree=child[1]
            father=self.global_env
        elif len(child)==3:
            classname=self.getVarNameFromAsttree(child[0])
            astTree=child[2]
            father=self.getVarNameFromAsttree(child[1].getChild(0))
            father=self.global_env.getValue(father)
            father=father.getEnv()
        else:
            raise InterpreterException("class asttree format wrong",astTree.getToken())
        return self.now_env.setValue(classname,Class(classname,astTree,father))
        
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
                return self.eval(left)//right
            if op=="%":
                right=self.eval(right)
                self.isDivideZero(right,astTree)
                return self.eval(left)%right
            if op=="=":
                env,leftname=self.resolve_lvalue(left)
                if leftname:
                    return env.setValue(leftname,self.eval(right))
                else:
                    raise InterpreterException("failed to set value of",left.getToken())
        return self.eval(astTree.child[0])
    def resolve_lvalue(self,left_asttree):
        env=self.now_env
        leftname=self.getVarNameFromAsttree(left_asttree)
        if left_asttree.getType()!="primary":
            #suppose left as a primary
            raise InterpreterException("Unable to get lvalue")
        if left_asttree.getChildNum()==0:
            pass
        else:
            env,leftname=self.do_pri(left_asttree,isLeft=True)
        return env,leftname
    def getVarNameFromAsttree(self,astTree):
        if type(astTree)==ASTfruit:
            token=astTree.getToken()
            if token.getType()=="IDENTIFIER":
                return token.getValue()
        return 0
    def do_pri(self,astTree,isLeft=False):
        num_child=astTree.getChildNum()
        child=astTree.getChild()
        if num_child==0 and type(astTree)==ASTfruit:
            varname=self.getVarNameFromAsttree(astTree)
            if varname:
                return self.now_env.getValue(varname)
            return astTree.getValue()
        elif astTree.getValue()=="lambda":
            return self.do_lambda(astTree)
        elif num_child>0:
            primary=astTree.getValue()
            cnt=0
            env=self.now_env
            for postfix in child:
                if postfix.getType()=="postfix":
                    primary=self.do_postfix(primary,postfix,env)
                elif postfix.getType()=="dot":
                    env,primary=self.do_dot(primary,postfix,env)
                    if isLeft and cnt==len(child)-1:
                        return env,self.getVarNameFromAsttree(postfix.getChild(0))
                    
                else:
                    return self.eval(postfix)
                cnt+=1
            return primary
        return self.eval(astTree.child[0])
    def init_env_classinstance(self,obj):
        instance=ClassInstance(obj.getEnv())
        self.now_env=instance.getEnv()
        self.eval(obj.getAsttree())
        self.now_env=instance.getFatherEnv()
        return instance
    def do_dot(self,primary,postfix,env):
        varname=postfix.getChild(0)
        varname=self.getVarNameFromAsttree(varname)
        obj=env.getValue(primary)
        #<obj>.<varname>
        #a.b.c.d
        if varname=="new":
            if not isinstance(obj,Class):
                raise InterpreterException("Only class can create instance")
            instance=self.init_env_classinstance(obj)
            return obj.getEnv(),instance
        else:
            if not isinstance(obj,ClassInstance):
                raise InterpreterException("You should make a instance from class before to use")
            env=obj.getEnv()
            return env,env.getValue(varname)



    def do_lambda(self,astTree):
        args=self.get_args(astTree.child[0])
        fun=astTree.child[1]
        return Function("lambda",args,fun,self.now_env)
    def do_postfix(self,primary,postfix,env):
        nowenv=self.now_env
        self.now_env=env
        fun_name=primary

        result=self.do_fun(fun_name,self.get_args(postfix))

        self.now_env=self.now_env
        return result
    def do_fun(self,fun,args):
        if isinstance(fun,str):
            fun:Function=self.now_env.getValue(fun)
        
        if isinstance(fun,NativeFunction):
            fun.setArgs(args)
            return self.nfm.eval(fun)
        
        self.now_env=fun.runInit(args)
        result=self.eval(fun.getASTtree())
        self.now_env=fun.runUnwind()
        
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