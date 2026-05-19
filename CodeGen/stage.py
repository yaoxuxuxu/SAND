import os
class Stage:
    def __init__(self,name,model):
        self.model=model
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
    def go_next_stage(self):
        pass

    def run(self,max_iter=100):
        if max_iter<0:
            max_iter=100
        for i in range(max_iter):
            res=self.model.send(self.config_prompt)
            self.end_context_index+=1
            if "!!!next stage!!!" in res:
                break
            if i == max_iter-1:
                break
            print(res)
            self.model.user_input()
            self.end_context_index+=1
        return self.model.getLastSolution()
    def clear_history(self):
        self.model.history=self.model.history[:self.start_context_index]
    
        
        