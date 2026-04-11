class Token:
    def __init__(self,linenumber=-1):
        self.stonetype=""
        self.linenumber=linenumber
    def isNumber(self):
        return False
    def isString(self):
        return False
    def isIdentifier(self):
        return False
    def getLineNumber(self):
        return self.linenumber
    def EOF():
        return "\n"
class NumberToken(Token):
    def __init__(self, linenumber=-1):
        super().__init__(linenumber)