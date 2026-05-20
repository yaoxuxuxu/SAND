from .stage import Stage
from .modelManager import ModelManager
import os
root_dir="./CodeGen/project"
def main():
    
    mm=ModelManager()
    #main prompt
    mm.history.append(mm.user("implement a fib function."))
    #question
    sum=Stage("question",mm).run(3,return_mode="summary")
    print(sum)
    #file arrange
    files=Stage("file_arrange",mm).run(return_mode="parse_json")
    #main coding
    for file,des in files.items():
        tmp_stage=Stage("code",mm)
        tmp_stage.config_prompt+="now we are writing:"+file
        code=tmp_stage.run(return_mode="parse_sand")
        with open(os.path.join(root_dir,file),"w+") as fp:
            fp.write(code)

    
if __name__ == "__main__":
   main()