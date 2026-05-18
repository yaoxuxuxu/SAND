from ..library import StandardLibrary
class File(StandardLibrary):
    def __init__(self):
        super().__init__()
        self.description="BuiltInLibrary:File"
    def read(self,args):
        #read(dir)
        dir=args[0]
        try:
            with open(dir,"r+") as fp:
                res=fp.read()
        except:
            self.raise_exception("Failed to read the file at\n"+str(dir))
        return res
    
    def write(self,args):
        #write(dir,text)
        dir=args[0]
        text=args[1]
        with open(dir,"w+") as fp:
            fp.write(text)