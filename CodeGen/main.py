from .stage import Stage
from .modelManager import ModelManager
import os
config_dir="./CodeGen/ConfigPrompts"
project_dir="./CodeGen/project"
def code_config():
    config=""
    with open(os.path.join(config_dir,"code_front.txt"),"r+") as fp:
        config+=fp.read()
    #add examples
    example_dir="./sand_code/sand_example"
    for example in os.listdir(example_dir):
        config+="\n```sand\n"
        with open(os.path.join(example_dir,example),"r+") as fp:
            config+=fp.read()
        config+="\n```\n"

    with open(os.path.join(config_dir,"code_back.txt"),"r+") as fp:
        config+=fp.read()
    return config
def debug_code():
    config=code_config()
    with open("config.txt","w+") as fp:
        fp.write(config)
def main(debug=False):
    if debug:
        debug_code()
    else:
        main_workflow()
def main_workflow():
    mm=ModelManager()
    #main prompt
    res=input("main prompt: ")
    mm.history.append(mm.user(res))
    #question
    sum=Stage("question",mm).run(3,return_mode="summary")
    #file arrange
    files=Stage("file_arrange",mm).run(return_mode="parse_json")
    #main coding
    for file,des in files.items():
        tmp_stage=Stage("code",mm,config=code_config)
        tmp_stage.config_prompt+="now the file is:"+file
        writting_dir=os.path.join(project_dir,file)
        code=tmp_stage.run(return_mode="parse_sand",file=writting_dir)
        with open(writting_dir,"w+") as fp:
            fp.write(code)

    
if __name__ == "__main__":
   main(debug=0)