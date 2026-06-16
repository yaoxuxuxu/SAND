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

class perfect_document(ModelManager):
    def __init__(self):
        super().__init__("gemma-4-31b-it")
        with open(os.path.join(config_dir,"document.txt")) as fp:
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