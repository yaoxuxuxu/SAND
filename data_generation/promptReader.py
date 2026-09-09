import re
class PromptReader:
    def __init__(self,dir=""):
        self.prompt_dir=dir
        self.data={}
        self.read()
    def get(self,varname):
        return self.data[varname]
    def read(self):
        with open(self.prompt_dir,"r+",encoding="utf-8") as fp:
            res=fp.read()
        pattern = re.compile(
        r"<prompt\s+([^\r\n>]+)>\n(.*?)\n<end>",
        re.DOTALL
        )
        m=pattern.findall(res)
        for pair in m:
            self.data[pair[0]]=pair[1]
        return


if __name__ == "__main__":
    pr=PromptReader("./data_generation/prompts")
    pr.read()
    print(pr.data)
