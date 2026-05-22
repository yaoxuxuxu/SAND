import os
from .formatParser import Parser
class Stage:
    def __init__(self,name,model):
        self.model=model
        self.parser=Parser()
        self.name=name
        #record message index for this stage
        self.start_context_index=len(self.model.history)
        self.end_context_index=self.start_context_index

        self.running_dir=os.path.dirname(os.path.abspath(__file__))
        self.config_prompt=self.config()
    def config(self):
        with open(os.path.join(self.running_dir, "ConfigPrompts", "main.txt"), "r+") as fp:
            main_config=fp.read()
        with open(os.path.join(self.running_dir, "ConfigPrompts", self.name + ".txt"), "r+") as fp:
            config_prompt=fp.read()
        return main_config+config_prompt
    def returnByMode(self,mode):
        if mode=="solution":
            return self.model.getLastSolution()
        if mode[0:6]=="parse_":
            #parse_xxx: xxx is the format.
            return self.parser.parse(mode[6:],self.model.getLastSolution())
        if mode=="summary":
            return self.summary()
        if mode=="remain_all":
            return "!!!RemainAll!!!"
        print(f"Unknown return mode: {mode}")
        return None
    def send(self):
        res=self.model.send(self.config_prompt)
        self.end_context_index+=1
        return res
    def user_input(self):
        self.model.user_input()
        self.end_context_index+=1
    def run(self,max_iter=100,return_mode="solution"):
        if max_iter<0:
            max_iter=100
        for i in range(max_iter):
            res=self.send()
            if "!!!next stage!!!" in res:
                break
            if i == max_iter-1:
                break
            print(res)
            self.user_input()
        
        result=self.returnByMode(return_mode)
        if result != "!!!RemainAll!!!":
            self.clear_history()
            self.model.history.append(self.model.assistant(str(result)))
        return result
    
    def clear_history(self):
        self.model.history=self.model.history[:self.start_context_index]
    def summary(self):
        res=self.model.send("please summarize the above conversation in few sentence.",
                            self.model.history[self.start_context_index:self.end_context_index])
        return res
        