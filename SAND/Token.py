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
