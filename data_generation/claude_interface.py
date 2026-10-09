from llmhacker.claude import Claude
import os
class ModelManager:
    def __init__(self,modelname=None):
        #modelname is meaningless
        self.history=""
        self.model=Claude()
    def user_add(self,text):
        if self.history!="":
            self.history+="\n\n"
        self.history+=text
    def send(self,config=None):
        if config:
            self.history=config+"\n\n"+self.history
        return self.model.send(self.history)
        

class fewshot(ModelManager):
    def __init__(self):
        super().__init__()
    class patched_document(ModelManager):
        def __init__(self):
            super().__init__()
            config_dir="./CodeGen/ConfigPrompts/"
            with open(os.path.join(config_dir,"patched.txt")) as fp:
                doc=fp.read()
            self.history=doc
            self.model=Claude()
                    