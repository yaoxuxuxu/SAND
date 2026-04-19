from asttree import ASTfruit,ASTnode
from StoneException import InterpreterException
from environment import Environment
class Interpreter:
    def __init__(self):
        self.global_env=Environment()
    def eval(self,astTree):
        if astTree.exp_type=="statement":
            return self.do_state(astTree)
        if astTree.exp_type=="expression":
            return self.do_expr(astTree)
        if astTree.exp_type=="primary":
            return self.do_pri(astTree)
        for i in astTree.child:
            last=self.eval(i)
        return last
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
                var=self.getVarNameFromAsttree(left)
                if var:
                    return self.global_env.setValue(var,self.eval(right))
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
                return self.global_env.getValue(varname)
            return astTree.getValue()
        return self.eval(astTree.child[0])
    def isDivideZero(self,value,astTree):
        if value==0:
            raise InterpreterException("Divide Zero!\n",astTree.getToken())
        return

if __name__ == "__main__":
    itpt=Interpreter()