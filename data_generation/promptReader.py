class PromptReader:
    def __init__(self):
        self.prompt_dir=""
        self.data={}
    def read(self):
        with open(self.prompt_dir,"r+",encoding="utf-8") as fp:
            res=fp.read()
