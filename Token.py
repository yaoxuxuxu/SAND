class Token:
    EOF=None
    def __init__(self,linenumber=-1):
        self.stonetype="None"
        self.value=None
        self.linenumber=linenumber
    def __str__(self):
        return f"(Type:Token.{self.stonetype},Value:{self.value},Line:{self.linenumber})"
    def getLineNumber(self):
        return self.linenumber
    def getValue(self):
        return self.value
    def getType(self):
        return self.stonetype
    
#set Token.EOF
EOF=Token()
EOF.value="\n"
Token.EOF=EOF

"""class NumberToken(Token):
    def __init__(self, linenumber=-1,value=0):
        super().__init__(linenumber)
        self.stonetype="NUMBER"
        self.value=value
class StringToken(Token):
    def __init__(self, linenumber=-1,value=""):
        super().__init__(linenumber)
        self.stonetype="STRING"
        self.value=value
class IDToken(Token):
    def __init__(self, linenumber=-1,value=""):
        super().__init__(linenumber)
        self.stonetype="IDENTIFIER"
        self.value=value"""