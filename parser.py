from Token import Token
from lexer import Lexer
from asttree import ASTnode,ASTleaf
from StoneException import StoneException,ParserException
#all of the [] part is not done
class Parser:
    BADMATCH="!bad match!"
    def __init__(self,code):
        self.lexer=Lexer(code)

    def parse(self):
        ASTlist=[]
        while 1:
            ASTtree=self.program()
            if ASTtree==self.BADMATCH:
                break
            ASTlist.append(ASTtree)
        if self.lexer.peek(0)!=Token.EOF:
            raise ParserException(self.lexer.peek(0))
        return ASTlist
    def match(self,rule):
        if type(rule)!=type([]):
            rule=[rule]
        if type(rule)!=type([]):
            raise TypeError("Parser.match.rule need to be list")
        token=self.lexer.peek(0)
        if token==Token.EOF:
            return 0
        if token.value in rule:
            return 1
        return 0
    def match_type(self,rule):
        if type(rule)!=type([]):
            rule=[rule]
        if type(rule)!=type([]):
            raise TypeError("Parser.match_type.rule need to be list")
        token=self.lexer.peek(0)
        if token==Token.EOF:
            return 0
        if token.stonetype in rule:
            return 1
        return 0
    def isOperator(self,token):
        op=r"+-*/% >= <= == && ||"
        if token==Token.EOF:
            return 0
        if type(token.value) == str:
            return token.value in op
        return 0
    def check_EOF(self):
        return self.lexer.peek(0)==Token.EOF
    def check_EOL(self):
        lasttoken=self.lexer.peek(-1)
        nowtoken=self.lexer.peek(0)
        if lasttoken == Token.EOF or nowtoken == Token.EOF:
            return 0
        return lasttoken.getLineNumber()!=nowtoken.getLineNumber()
    def getErrorLine(self):
        token=self.lexer.peek(0)
        if token=="EOF":
            return "last_line"
        return token.getLineNumber()
    def program(self):
        child=[self.statement()]
        if child[0]==self.BADMATCH:
            return self.BADMATCH
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
                tmp=self.statement()
                if tmp==self.BADMATCH:
                    break
                child.append(tmp)
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
            if child[0]==self.BADMATCH:
                return self.BADMATCH
        return self.createStem("statement",child)
    def expression(self):
        child=[self.factor()]
        if child[0]==self.BADMATCH:
            return self.BADMATCH
        while self.isOperator(self.lexer.peek(0)):
            token=self.lexer.read()
            child.append(self.token2leaf(token,"OP"))
            child.append(self.factor())
        return self.createStem("expr",child)
    def factor(self):
        if self.match("-"):
            token=self.lexer.read()
            tmp=self.primary()
            if tmp==self.BADMATCH:
                raise StoneException("syntax error at",token.getLineNumber())
            return self.createStem("factor",[self.token2leaf(token),self.primary()])
        tmp=self.primary()
        if tmp==self.BADMATCH:
            return self.BADMATCH
        return self.createStem("factor",[tmp])
    def primary(self):
        if self.match("("):
            #did not put () into ASTtree
            self.lexer.read()
            child=[self.expression()]
            if self.match(")"):
                self.lexer.read()
            else:
                raise ParserException("bracket is not matched")
            return self.createStem("primary",child)
        else:
            if self.match_type(["NUMBER","IDENTIFIER","STRING"]):
                token=self.lexer.read()
                return self.token2leaf(token)
            else:
                return self.BADMATCH
    def createStem(self,terminal="auto",child=[]):
        tmp=ASTnode()
        tmp.exp_type=terminal
        tmp.child=child
        return tmp
    def token2leaf(self,token,exp_type="primary"):
        #print(token,exp_type,"is used")
        tmp=ASTleaf(token.value)
        tmp.exp_type=exp_type
        return tmp
            
        
    def isInRange(self,cnt,r):
        if cnt+r > len(self.ASTlist):
            return 0
        return 1
    
if __name__ == "__main__":
    dir="./sand_code/ez_plus.sand"
    with open(dir,"r+") as fp:
        res=fp.read()
    parser=Parser(res)
    res=parser.parse()
    for i in res:
        print(i)
