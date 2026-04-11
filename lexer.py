import re
from Token import Token
class Lexer:
    def __init__(self,code_text):
        self.tokens=self.get_tokens(code_text)
    def get_tokens(self,code):
        line=0
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
            print(token_type,word)
        return
        token=[]
        for i in word:
            token.append(self.put_word_to_token(i,line))
    def put_word_to_token(self,word,line):
        return token
    def read(self):
        if len(self.tokens)==0:
            return Token.EOF
        token=self.tokens[0]
        self.tokens.pop(0)
        return token

if __name__ == "__main__":
    lexer=Lexer()
    with open("./test.stone","r+") as fp:
        res=fp.read()