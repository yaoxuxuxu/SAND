from Token import Token
from lexer import Lexer
from asttree import ASTnode,ASTleaf
class Parser:
    def __init__(self,code):
        self.lexer=Lexer(code)
        token=self.lexer.get_tokens()
        self.ASTlist=[]

        self.parse()
    def parse(self):
        ASTtree=self.program()
    def match(self,word):
        if self.lexer.peek(0)==word:
            return 1
        return 0

    def program(self):
        if not self.match(";") and not self.match("EOF"):
            statement=self.statement()
            
        tmp=ASTnode()
        tmp.exp_type="program"
        
    def primary(self):
        cnt=0
        while 1:
            if self.isInRange(cnt,3) and self.ASTlist[]:

    def isInRange(self,cnt,r):
        if cnt+r > len(self.ASTlist):
            return 0
        return 1
    
if __name__ == "__main__":
    with open("./test.stone","r+") as fp:
        res=fp.read()
    parser=Parser(res)
