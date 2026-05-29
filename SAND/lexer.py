import re
from .Token import Token,EOF
from .StoneException import StoneException
class Lexer:
    def __init__(self,code_text):
        self.tokens=[]
        self.last_token=None
        self.get_tokens(code_text)
    def get_tokens(self,code):
        line=1
        for i in code.split("\n"):
            self.get_words_from_code(i,line)
            line+=1
    def get_words_from_code(self,code,line):
        regex = r"""
                \s*(?:
                    (?P<COMMENT>//.*) |
                    (?P<NUMBER>\d+\.\d+|\d+)  |
                    (?P<STRING>"(?:\\"|\\\\|\\n|[^"])*") |
                    (?P<BOOL>true|false) |
                    (?P<IDENTIFIER>[A-Za-z_][A-Za-z0-9_]*) |
                    (?P<OP>!=|==|<=|>=|&&|\|\||[^\w\s])
                    )
                """
        pattern=re.compile(regex,re.VERBOSE)
        for m in pattern.finditer(code):
            token_type=m.lastgroup
            word=m.group(0).strip()
            if token_type=="NUMBER":
                try:
                    value=float(word)
                except:
                    raise StoneException("Failed to get number token",line)
                self.createToken("NUMBER",value,line)
            elif token_type=="STRING":
                word=word.replace('"','')
                word=self.strEscape(word)
                self.createToken("STRING",word,line)
            elif token_type=="BOOL":
                if word=="ture":
                    word=True
                else:
                    word=False
                self.createToken("BOOL",word,line) 
            elif token_type == "IDENTIFIER":
                self.createToken("IDENTIFIER",word,line)
            elif token_type == "OP":
                self.createToken("OP",word,line)
            elif token_type == "COMMENT":
                pass
            else:
                raise StoneException("Failed to get the type from a word",line)
    def createToken(self,stonetype,value,line):
        tmp=Token(line)
        tmp.stonetype=stonetype
        tmp.value=value
        self.tokens.append(tmp)
        return
    def getTokens(self):
        return self.tokens
    def strEscape(self,word):
        word=word.replace(r'\\','\\')
        word=word.replace(r'\n','\n')
        return word
    def read(self):
        if len(self.tokens)==0:
            return Token.EOF
        token=self.tokens[0]
        self.last_token=self.tokens.pop(0)
        return token
    def peek(self,offset=0):
        if offset>len(self.tokens)-1:
            return Token.EOF
        if offset==-1:
            return self.last_token
        if offset<-1:
            raise StoneException("peek only can peek token [-1:n]")
        return self.tokens[offset]

if __name__ == "__main__":
    with open("./test.stone","r+") as fp:
        res=fp.read()
        lexer=Lexer(res)
    cnt=0
    while 1:
        token=lexer.read()
        if token==Token.EOF:
            break
        if cnt>50:
            break
        print(token)