from .stage import Stage
from .modelManager import ModelManager
def main():
    mm=ModelManager()
    mm.history.append(mm.user("implement a fib function."))
    Stage("question",mm).run(3)
    Stage("file_arrange",mm).run()
    
if __name__ == "__main__":
    main()