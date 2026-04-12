from lexer import Lexer
from Token import Token
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
    
    
