from .modelManager import ModelManager
import os
config_dir="./CodeGen/ConfigPrompts/"
class baseline(ModelManager):
    def __init__(self):
        super().__init__("gemma-4-31b-it")
        self.user_add("""you should only use the programming language sand.
                      sand is a self made script programming language and it is similar to 
                      the programming language STONE.Stone is a self made PL in a PL book.
                      its writter is Professor Chiba from Tokyo University, Chiba Software Lab.""")

class bnf_only(ModelManager):
    def __init__(self):
        super().__init__("gemma-4-31b-it")
        with open(os.path.join(config_dir,"ebnf.txt")) as fp:
            bnf=fp.read()
        self.user_add("This is the bnf of programming language SAND.")
        self.user_add(bnf)

class nl_only(ModelManager):
    def __init__(self):
        super().__init__("gemma-4-31b-it")
        with open(os.path.join(config_dir,"nl.txt")) as fp:
            nl=fp.read()
        self.user_add("This is a description of programming language SAND.")
        self.user_add(nl)
class document(ModelManager):
    def __init__(self):
        super().__init__("gemma-4-31b-it")
        with open(os.path.join(config_dir,"document.txt")) as fp:
            doc=fp.read()
        self.user_add(doc)
class patched_document(ModelManager):
    def __init__(self):
        super().__init__("gemma-4-31b-it")
        with open(os.path.join(config_dir,"patched.txt")) as fp:
            doc=fp.read()
        self.user_add(doc)


class example_only(ModelManager):
    def __init__(self):
        super().__init__()
        self.user_add("These are some example of programming language SAND.")
        self.user_add(self.code_config())
    def code_config(self):
        config="<example>"
        #add examples
        example_dir="./sand_code/sand_example"
        for example in os.listdir(example_dir):
            config+="\n```sand\n"
            with open(os.path.join(example_dir,example),"r+") as fp:
                config+=fp.read()
            config+="\n```\n"
        config+="</example>"

        return config
    


if __name__ == "__main__":
    model=patched_document()
    code=model.send("write a program,input a lucky number,generate today's fortune.")
    with open("./CodeGen/project/testcode.sand","w+",encoding="utf-8") as fp:
            fp.write(code)
    while 1:
        res=input()
        if res == "exit":
            break
        model.user_add(res)
        with open("./CodeGen/project/testcode.sand","w+",encoding="utf-8") as fp:
            fp.write(code)
        
    print("done")