import re
from Token import Token,NumberToken,StringToken,IDToken
from StoneException import StoneException
class Lexer:
    def __init__(self,code_text):
        self.tokens=[]
        self.get_tokens(code_text)
    def get_tokens(self,code):
        line=1
        for i in code.split("\n"):
            self.get_words_from_code(i,line)
            line+=1
    def get_words_from_code(self,code,line):
        regex = r"""
                \s*(?://.* |
                (?P<NUMBER>[0-9]+) |
                (?P<STRING>"(?:\\"|\\\\|\\n|[^"])*") |
                (?P<IDENTIFIER>[A-Za-z_][A-Za-z0-9_]* |
                ==|<=|>=|&&|\|\| | [^\w\s]
                ))
                """
        pattern=re.compile(regex,re.VERBOSE)
        for m in pattern.finditer(code):
            token_type=m.lastgroup
            word=m.group(0).strip()
            if token_type=="NUMBER":
                try:
                    value=int(word)
                except:
                    raise StoneException("Failed to get number token",line)
                self.tokens.append(NumberToken(line,value))
            elif token_type=="STRING":
                self.tokens.append(StringToken(line,word))
            elif token_type=="IDENTIFIER":
                self.tokens.append(IDToken(line,word))
            else:
                raise StoneException("Failed to get the type from a word",line)
    def read(self):
        if len(self.tokens)==0:
            return Token.EOF
        token=self.tokens[0]
        self.tokens.pop(0)
        return token
    def peek(self,offset):
        if offset>len(self.tokens):
            return Token.EOF
        return self.tokens[offset]

if __name__ == "__main__":
    lexer=Lexer()
    with open("./test.stone","r+") as fp:
        res=fp.read()