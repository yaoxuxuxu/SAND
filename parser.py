from Token import Token
from lexer import Lexer
from asttree import ASTnode,ASTleaf
from StoneException import StoneException
#all of the [] part is not done
class Parser:
    def __init__(self,code):
        self.lexer=Lexer(code)

    def parse(self):
        ASTtree=self.program()
        return ASTtree
    def match(self,rule):
        if type(rule)!=type([]):
            rule=[rule]
        if type(rule)!=type([]):
            raise TypeError("Parser.match.rule need to be list")
        token=self.lexer.peek(0)
        if token.value in rule:
            return 1
        return 0
    def match_type(self,rule):
        if type(rule)!=type([]):
            rule=[rule]
        if type(rule)!=type([]):
            raise TypeError("Parser.match_type.rule need to be list")
        token=self.lexer.peek(0)
        if token.stonetype in rule:
            return 1
        return 0
    def check_EOL(self):
        nowtoken=self.lexer.peek(0)
        nexttoken=self.lexer.peek(1)
        print(nowtoken,nexttoken)
        if nowtoken == Token.EOF or nexttoken == Token.EOF:
            return 1
        return nowtoken.getLineNumber()!=nexttoken.getLineNumber()
    def getErrorLine(self):
        token=self.lexer.peek(0)
        if token=="EOF":
            return "last_line"
        return token.getLineNumber()
    def program(self):
        child=[self.statement()]
        ASTtree=self.createStem("program",child)
        if self.match(";"):
            self.lexer.read()
        return ASTtree
    def block(self):
        if self.match("{"):
            self.lexer.read()
            child=[self.statement()]
            while True:
                if self.match(";"):
                    self.lexer.read()
                elif not self.check_EOL():
                    break
                child.append(self.statement())
            if self.match("}"):
                self.lexer.read()
            else:
                token=self.lexer.read()
                print(token)
                raise StoneException("expected } at",self.getErrorLine())
            return self.createStem("block",child)
    def statement(self):
        if self.match("if"):
            self.lexer.read()
            child=[self.expression(),self.block()]
            if self.match("else"):
                self.lexer.read()
                child.append(self.block())
        elif self.match("while"):
            self.lexer.read()
            child=[self.expression(),self.block()]
        else:
            child=[self.expression()]
        return self.createStem("statement",child)
    def expression(self):
        child=[self.factor()]
        while self.match_type("OP"):
            token=self.lexer.read()
            child.append(self.token2leaf(token,"OP"))
            child.append(self.factor())
        return self.createStem("expr",child)
    def factor(self):
        if self.match("-"):
            token=self.lexer.read()
            return self.createStem("factor",[self.token2leaf(token),self.primary()])
        return self.primary()
    def primary(self):
        if self.match("("):
            #did not put () into ASTtree
            self.lexer.read()
            child=self.expression()
            if self.match(")"):
                raise StoneException()
            return self.createStem("primary",child)
        else:
            if self.match_type(["NUMBER","IDENTIFIER","STRING"]):
                token=self.lexer.read()
                return self.token2leaf(token)
            else:
                print(token)
                raise StoneException("Bad Token",token.getLineNumber())
    def createStem(self,terminal="auto",child=[]):
        tmp=ASTnode()
        tmp.exp_type=terminal
        tmp.child=child
        return tmp
    def token2leaf(self,token,exp_type="primary"):
        tmp=ASTleaf(token.value)
        tmp.exp_type=exp_type
        return tmp
            
        
    def isInRange(self,cnt,r):
        if cnt+r > len(self.ASTlist):
            return 0
        return 1
    
if __name__ == "__main__":
    with open("./test.stone","r+") as fp:
        res=fp.read()
    parser=Parser(res)
    for i in range(2):
        res=parser.parse()
        print(res)
