from Token import Token
from lexer import Lexer
from asttree import ASTnode,ASTfruit
from StoneException import StoneException,ParserException
#all of the [] part is not done
class Parser:
    BADMATCH="!bad match!"
    def __init__(self,code):
        self.lexer=Lexer(code)
        self.precedence={"=":10,
                         "||":20,
                         "&&":30,
                         "==":40,"!=":40,
                         "<":50,"<=":50,">":50,">=":50,
                         "+":60,"-":60,
                         "*":70,"/":70,"%":70
                        }
    def parse(self):
        ASTlist=[]
        while 1:
            ASTtree=self.program()
            if ASTtree==self.BADMATCH:
                break
            ASTlist.append(ASTtree)
        if self.peek()!=Token.EOF:
            raise ParserException("",self.peek())
        return ASTlist
    def consume(self):
        return self.lexer.read()
    def peek(self,offset=0):
        return self.lexer.peek(offset)
    def match(self,rule):
        if type(rule)!=type([]):
            rule=[rule]
        if type(rule)!=type([]):
            raise TypeError("Parser.match.rule need to be list")
        token=self.peek(0)
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
        token=self.peek(0)
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
        return self.peek(0)==Token.EOF
    def check_EOL(self):
        lasttoken=self.peek(-1)
        nowtoken=self.peek(0)
        if lasttoken == Token.EOF or nowtoken == Token.EOF:
            return 0
        return lasttoken.getLineNumber()!=nowtoken.getLineNumber()
    def getErrorLine(self):
        token=self.peek(0)
        if token=="EOF":
            return "last_line"
        return token.getLineNumber()
    def program(self):
        child=[self.statement()]
        if child[0]==self.BADMATCH:
            return self.BADMATCH
        ASTtree=self.createNode("program",child)
        if self.match(";"):
            self.consume()
        return ASTtree
    def block(self):
        if self.match("{"):
            self.consume()
            child=[self.statement()]
            while True:
                if self.match(";"):
                    self.consume()
                elif not self.check_EOL():
                    break
                tmp=self.statement()
                if tmp==self.BADMATCH:
                    break
                child.append(tmp)
            if self.match("}"):
                self.consume()
            else:
                token=self.consume()
                print(token)
                raise StoneException("expected } at",self.getErrorLine())
            return self.createNode("block",child)
    def statement(self):
        if self.match("if"):
            iftoken=self.consume()
            child=[self.expression(),self.block()]
            if self.match("else"):
                else_token=self.consume()
                child.append(self.block())
            return self.createNode("statement",child,iftoken)

        elif self.match("while"):
            whiletoken=self.consume()
            child=[self.expression(),self.block()]
            return self.createNode("statement",child,whiletoken)
        else:
            child=[self.expression()]
            if child[0]==self.BADMATCH:
                return self.BADMATCH
            return self.createNode("statement",child)
    """def expression(self):
        #old expr
        child=[self.factor()]
        if child[0]==self.BADMATCH:
            return self.BADMATCH
        while self.isOperator(self.peek(0)):
            token=self.consume()
            child.append(self.token2leaf(token,"OP"))
            child.append(self.factor())
        return self.createNode("expr",child)"""
    def expression(self,min_prec=0):
        #pratt_expr
        left=self.factor()
        if left==self.BADMATCH:
            return self.BADMATCH
        while True:
            opToken=self.peek()
            op=opToken.getValue()
            if op not in self.precedence:
                break
            prec=self.precedence[op]
            if prec<min_prec:
                break
            self.consume()
            if op=="=":
                right= self.expression(prec-1)
            else:
                right = self.expression(prec+1)
            left = self.createNode("expression",[left,right],opToken)
        return left
            
    def factor(self):
        if self.match("-"):
            token=self.consume()
            tmp=self.primary()
            if tmp==self.BADMATCH:
                raise StoneException("syntax error at",token.getLineNumber())
            return self.createNode("factor",[self.token2leaf(token),self.primary()])
        return self.primary()
    def primary(self):
        if self.match("("):
            #did not put () into ASTtree
            self.consume()
            child=[self.expression()]
            if self.match(")"):
                self.consume()
            else:
                raise ParserException("bracket is not matched",self.peek(0))
            return self.createNode("primary",child)
        else:
            if self.match_type(["NUMBER","IDENTIFIER","STRING"]):
                token=self.consume()
                return self.createNode("primary",[],token)
            else:
                return self.BADMATCH
    def createNode(self,terminal="auto",child=[],token=None):
        if token:
            tmp=ASTfruit(token)
        else:
            tmp=ASTnode()
        tmp.exp_type=terminal
        tmp.child=child
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
