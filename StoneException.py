from Token import Token
class StoneException(Exception):   
    def __init__(self, message, line=None):
        super().__init__(message)
        self.line = line
    def __str__(self):
        if self.line:
            return f"[line {self.line}] {self.args[0]}"
        return self.args[0]
class ParserException(StoneException):
    def __init__(self,token,message=""):
        message+="Parse Fail at '"+str(token.value)+"'"
        super().__init__(message,token.getLineNumber())
