from .asttree import ASTfruit,ASTnode
from .StoneException import InterpreterException
from .environment import Environment,TreeEnv
from .function import Function,NativeFunction,NativeFunctionManager
from .oop import Class,ClassInstance
from .vector import Vector
from .parser import Parser
from .library import BuiltInLibraryManager,BuiltInLibrary
import os,time,types
class Interpreter:
    def __init__(self,dir=""):
        self.global_env=Environment()
        self.set_native_function()
        self.bilm=BuiltInLibraryManager()
        self.now_env=self.global_env
        self.dir=dir
        

    def debug(self,astTree):
        print(self.now_env.var)
        print(self.now_env)
        #print(astTree)
        time.sleep(0.5)
        

    def eval(self,astTree):
        if astTree.getType()=="import_lib":
            return self.import_lib(astTree)
        if astTree.getType()=="function":
            return self.create_fun(astTree)
        if astTree.getType()=="class":
            return self.create_class(astTree)
        if astTree.getType()=="statement":
            return self.do_state(astTree)
        if astTree.getType()=="expression":
            return self.do_expr(astTree)
        if astTree.getType()=="factor":
            return self.do_factor(astTree)
        if astTree.getType()=="primary":
            return self.do_pri(astTree)
        if astTree.getType()=="primary_array":
            return self.create_array(astTree)
        last=None
        for i in astTree.child:
            last=self.eval(i)

        #self.debug(astTree)
        return last
    def set_native_function(self):
        self.nfm=NativeFunctionManager()
        for i in self.nfm.fun_list:
            self.global_env.setValue(i,NativeFunction(i,[]))
    def getLibEnvFromDir(self,dir):
        try:
            with open(dir,"r+") as fp:
                code=fp.read()
        except:
            return None
        parser=Parser(code)
        itpt=Interpreter(os.path.dirname(dir))
        for program in parser.parse():
            itpt.eval(program)
        return itpt.global_env
    def try_import(self,astTree):
        name=self.getVarNameFromAsttree(astTree)
        dir=os.path.join(self.dir,name+".sand")
        env=self.getLibEnvFromDir(dir)
        if env==None:
            if self.bilm.isBuiltInLibrary(name):
                env=self.bilm.importLib(name)
            else:
                raise InterpreterException("Can't Find Library "+name)
        return name,env
    def eval_import(self,astTree):
        libs=astTree.getChild()
        for lib in libs:
            name,env=self.try_import(lib)
            if isinstance(env,BuiltInLibrary):
                self.now_env.setValueForce(name,env)
            else:
                self.now_env.setValueForce(name,ClassInstance(env))

    def eval_from(self,astTree):
        name,env=self.try_import(astTree.getChild(0))
        objects=astTree.getChild(1).getChild()
        #built in library support
        if isinstance(env,BuiltInLibrary):
            funs=env.returnAllMethod()
            if len(objects)==1 and objects[0].getValue()=="ALL":
                for varname,value in funs:
                    self.now_env.setValueForce(varname,value)
                return
            for object in objects:
                name=self.getVarNameFromAsttree(object)
                self.now_env.setValueForce(name,env.importFunByName(name))  
            return
        #normal library support
        if len(objects)==1 and objects[0].getValue()=="ALL":
            for varname,value in env.var.items():
                self.now_env.setValueForce(varname,value)
            return
        for object in objects:
            name=self.getVarNameFromAsttree(object)
            self.now_env.setValueForce(name,env.getValue(name))
        return
    def import_lib(self,astTree):
        astTree=astTree.getChild(0)
        if astTree.getType()=="from":
            self.eval_from(astTree)
        elif astTree.getType()=="import":
            self.eval_import(astTree)
        else:
            raise InterpreterException("unable to eval import_lib statement, Parser has sth. wrong")
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
        else:
            raise InterpreterException("class asttree format wrong",astTree.getToken())
        init_asttree=[]
        functions=[]
        #seperate functions and non functions
        for sentence in astTree.getChild():
            if sentence.getType()=="function":
                functions.append(sentence)
            else:
                init_asttree.append(sentence)
        classObject=self.now_env.setValue(classname,Class(classname,init_asttree,father))
        #set functions
        self.eval_with_env(functions,classObject.getEnv())
        return classObject
    def eval_with_env(self,astTree,env):
        nowenv=self.now_env
        self.now_env=env
        result=None
        if isinstance(astTree,list):
            for sentence in astTree:
                result=self.eval(sentence)
        else:
            result=self.eval(astTree)
        self.now_env=nowenv
        return result
    def create_fun(self,astTree):
        name=astTree.child[0].getValue()
        param=astTree.child[1]
        fun=astTree.child[2]
        args=self.get_args(param)
        return self.env_add_fun(name,args,fun)
    def create_array(self,astTree):
        values=[]
        elements=astTree.getChild(0)
        for expr in elements.getChild():
            values.append(self.eval(expr))
        return Vector(values)

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
        while self.eval(astTree.child[0]):
            self.eval(astTree.child[1])
        return None
    def do_factor(self,astTree):
        op=astTree.getValue()
        if op=="-":
            return -self.eval(astTree.getChild(0))
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
            if op=="==":
                return self.eval(left)==self.eval(right)
            if op=="/":
                right=self.eval(right)
                self.isDivideZero(right,astTree)
                return self.eval(left)//right
            if op=="%":
                right=self.eval(right)
                self.isDivideZero(right,astTree)
                return self.eval(left)%right
            if op=="=":
                left=self.resolve_lvalue(left)
                right=self.eval(right)
                lefttype=left[0]
                
                if lefttype=="normal":
                    #(normal,name)
                    varname=[1]
                    return self.now_env.setValue(left[1],right)
                if lefttype=="class":
                    #(class,env,varname)
                    env=left[1]
                    varname=left[2]
                    return env.setValue(varname,right)
                if lefttype=="array":
                    #(normal,vector,index)
                    vector=left[1]
                    index=left[2]
                    self.array_check(index,vector)
                    return vector.setValueByIndex(index,right)
                
        return self.eval(astTree.child[0])
    def resolve_lvalue(self,left_asttree):
        leftname=self.getVarNameFromAsttree(left_asttree)
        if left_asttree.getType()!="primary":
            #suppose left as a primary
            raise InterpreterException("Unable to get lvalue")
        if left_asttree.getChildNum()==0:
            return ("normal",leftname)
        else:
            return self.do_pri(left_asttree,isLeft=True)
    def getVarNameFromAsttree(self,astTree):
        if type(astTree)==ASTfruit:
            token=astTree.getToken()
            if token.getType()=="IDENTIFIER":
                return token.getValue()
        return 0
    def do_pri(self,astTree,isLeft=False):
        if astTree.getValue()=="lambda":
            return self.do_lambda(astTree)
        else:
            return self.seperate_pri(astTree,isLeft)
    def seperate_pri(self,astTree,isLeft=False):
        token=astTree.getToken()
        if token==None:
            #expression like (a+b).something or (a+b)[something]
            if not astTree.hasChild():
                return None
            primary=self.eval(astTree.getChild(0))
            return self.do_decorate_var(primary,astTree.getChild(),isLeft)
        elif token.getType()=="NUMBER":
            return token.getValue()
        elif token.getType()=="STRING":
            return token.getValue()
        elif token.getType()=="IDENTIFIER":
            varname=self.getVarNameFromAsttree(astTree)
            if varname=="return_all":
                print("123456!!")
                return ClassInstance(self.now_env)
            primary=self.now_env.getValue(varname)
            return self.do_decorate_var(primary,astTree.getChild(),isLeft)
        else:
            raise InterpreterException("Unknown primary!",token)
    def do_decorate_var(self,primary,child,isLeft=False):
        
        env=self.now_env
        cnt=0
        for postfix in child:
            if postfix.getType()=="postfix":
                primary=self.do_postfix(primary,postfix,env)
            elif postfix.getType()=="dot":
                env,primary=self.do_dot(primary,postfix,env)
                if isLeft and cnt==len(child)-1:
                    return ("class",env,self.getVarNameFromAsttree(postfix.getChild(0)))
            elif postfix.getType()=="array":
                if isLeft and cnt==len(child)-1:
                    return ("array",primary,self.eval(postfix.getChild(0)))
                primary=self.do_array(primary,postfix,env)
            cnt+=1
        return primary
    def create_classinstance(self,obj):
        instance=ClassInstance(obj.getEnv())
        self.eval_with_env(obj.getAsttree(),instance.getEnv())
        #this
        instance.env.setValueForce("this",instance)
        return instance
    def array_check(self,num,vector):
        if not isinstance(vector,Vector):
            raise InterpreterException("Bad Array")
        if not isinstance(num,int):
            raise InterpreterException("Array index must be int")
        if num<0:
            raise InterpreterException("Negetive index not supported")
        if num>=len(vector):
            raise InterpreterException("index '"+str(num)+"' out of range")
        return True
    def do_array(self,primary,postfix,env):
        if isinstance(primary,str):
            primary=env.getValue(primary)
        index=postfix.getChild(0)
        index=self.eval(index)
        self.array_check(index,primary)
        #primary[]
        return primary.getValueByIndex(index)
        
    def do_dot(self,primary,postfix,env):
        nextpri=postfix.getChild(0)
        nextpri=self.getVarNameFromAsttree(nextpri)
        #<primary>.<nextpri>
        #special case
        if isinstance(primary,BuiltInLibrary):
            return env,primary.importFunByName(nextpri)
        if isinstance(primary,Vector):
            return env,primary.fetch_method(nextpri)
        #example:a.b.c.d
        if nextpri=="new":
            if not isinstance(primary,Class):
                raise InterpreterException("Only class can create instance")
            instance=self.create_classinstance(primary)
            return primary.getEnv(),instance
        else:
            if not isinstance(primary,ClassInstance):
                print(primary,nextpri,env.var)
                raise InterpreterException("You should make a instance from class before to use")
            env=primary.getEnv()
            primary=env.getValue(nextpri)
            if isinstance(primary,Function):
                primary=primary.copy()
                primary.setEnv(env)
            return env,primary



    def do_lambda(self,astTree):
        args=self.get_args(astTree.child[0])
        fun=astTree.child[1]
        return Function("lambda",args,fun,self.now_env)
    def do_postfix(self,primary,postfix,env):
        args=self.get_args(postfix)
        fun=primary
        result=self.do_fun(fun,args)
        return result
    def do_fun(self,fun,args):
        if isinstance(fun,NativeFunction):
            fun.setArgs(args)
            return self.nfm.eval(fun)
        if isinstance(fun, (types.MethodType,types.FunctionType)):
            return fun(args)
        env=fun.runInit(args)
        #print(fun.getName(),self.now_env.var)
        result=self.eval_with_env(fun.getASTtree(),env)
        fun.runUnwind()
        #print(fun.getName(),self.now_env.var)

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