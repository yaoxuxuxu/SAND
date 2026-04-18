from asttree import ASTfruit,ASTnode
from StoneException import InterpreterException
class Interpreter:
    def __init__(self):
        pass
    def eval(self,astTree):
        if astTree.exp_type=="expression":
            return self.do_expr(astTree)
        if astTree.exp_type=="primary":
            return self.do_pri(astTree)
        for i in astTree.child:
            return self.eval(i)
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
                right=self.eval(right,astTree)
                self.isDivideZero(right)
                return self.eval(left)%right
    def do_pri(self,astTree):
        if len(astTree.child)==0 and type(astTree)==ASTfruit:
            return astTree.getValue()
        for i in astTree.child:
            return self.eval(i)
    def isDivideZero(self,value,astTree):
        if value==0:
            raise InterpreterException("Divide Zero!\n",astTree.getToken())
        return

if __name__ == "__main__":
    itpt=Interpreter()