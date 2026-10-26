from .llm_interface import ModelManager,fewshot

class DiversityMaker:
    def __init__(self):
        pass
    def generate_prefix(self):
        return "summarize"
    def generate_suffix(self):
        pass


diversity_maker=DiversityMaker()

class ProblemLister:
    def __init__(self):
        #setting
        self.savefile="data_generation/ProblemLister"
        #var

        self.problemlist=[]
    
