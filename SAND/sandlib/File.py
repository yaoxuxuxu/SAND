from ..library import StandardLibrary
from ..StoneException import LibException
import os
class File(StandardLibrary):
    def __init__(self,work_dir):
        super().__init__()
        self.work_dir=work_dir
        self.description="BuiltInLibrary:File"
    def read(self,dir):
        dir=os.path.join(self.work_dir,dir)
        try:
            with open(dir,"r+") as fp:
                res=fp.read()
        except:
            self.raise_exception("Failed to read the file at\n"+str(dir))
        return res
    
    def write(self,dir,text):
        dir=os.path.join(self.work_dir,dir)
        with open(dir,"w+") as fp:
            fp.write(text)
    def remove(self,dir):
        dir=os.path.join(self.work_dir,dir)
        try:
            os.remove(dir)
        except:
            self.raise_exception(f"File '{dir}' not found.")
    def exist(self,dir):
        dir=os.path.join(self.work_dir,dir)
        return os.path.exists(dir)