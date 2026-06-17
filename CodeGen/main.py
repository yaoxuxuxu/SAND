from .stage import Stage
from .fewshot import perfect_document
from .modelManager import ModelManager
import os
config_dir="./CodeGen/ConfigPrompts"
project_dir="./CodeGen/project"
def code_config():
    config=""
    with open(os.path.join(config_dir,"code_front.txt"),"r+") as fp:
        config+=fp.read()
    #add examples
    with open(os.path.join(config_dir,"document.txt"),"r+") as fp:
        config+=fp.read()

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
    mm=ModelManager("gemma-4-31b-it")
    #main prompt
    res=input("main prompt: ")
    mm.user_add(res)
    #question
    sum=Stage("question",mm).run(3,return_mode="summary")
    #file arrange
    files=Stage("file_arrange",mm).run(return_mode="parse_json")
    #main coding
    for file,des in files.items():
        tmp_stage=Stage("code",mm,config=code_config)
        tmp_stage.config_prompt+="now the file is:"+file
        writting_dir=os.path.join(project_dir,file)
        code=tmp_stage.run(return_mode="parse_sand",file=writting_dir,withoutInput=True)
        with open(writting_dir,"w+") as fp:
            fp.write(code)

    
if __name__ == "__main__":
   main(debug=0)