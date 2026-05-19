from .stage import Stage
from .modelManager import ModelManager
from .formatParser import Parser
def main():
    mm=ModelManager()
    mm.history.append(mm.user("implement a fib function."))
    #Stage("question",mm).run(3)

    file_stage=Stage("file_arrange",mm)
    result=file_stage.run()
    result=Parser().parse("json",result)
    print(result)


    
if __name__ == "__main__":
   main()