from .Token import Token
class StoneException(Exception):   
    def __init__(self, message, line=None):
        super().__init__(message)
        self.line = line
    def __str__(self):
        if self.line:
            return f"[line {self.line}] {self.args[0]}"
        return self.args[0]
class ParserException(StoneException):
    def __init__(self,message="",token=Token.EOF):
        message+="\nParse Fail at '"+str(token.value)+"'"
        super().__init__(message,token.getLineNumber())
class InterpreterException(StoneException):
    def __init__(self,message="",token=Token.EOF):
        message+="\nEval Fail at '"+str(token.value)+"'"
        super().__init__(message,token.getLineNumber())
class FunctionException(StoneException):
    def __init__(self,message=""):
        message+="\nFunction Error\n"+message
        super().__init__(message)
class LibException(StoneException):
    def __init__(self, des,message, line=None):
        message=des+"\n"+message
        super().__init__(message)