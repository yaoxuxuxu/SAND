class StoneException(Exception):   
    def __init__(self, message, line=None):
        super().__init__(message)
        self.line = line
    def __str__(self):
        if self.line:
            return f"[line {self.line}] {self.args[0]}"
        return self.args[0]