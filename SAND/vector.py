from .StoneException import StoneException
class Vector:
    def __init__(self,value:list=[]):
        self.value=value
    def __len__(self):
        return len(self.value)
    def __str__(self):
        return str(self.value)
    def fetch_method(self,name):
        try:
            method=getattr(self,name)
        except:
            raise StoneException("No method called"+name)
        return method
    def append(self,args):
        self.value.append(args[0])
    def length(self,args):
        if len(args)!=0:
            raise StoneException("Wrong number of arguments") 
        return len(self.value)
    def pop(self,args):
        if len(args)!=1:
            raise StoneException("Wrong number of arguments")
        if not isinstance(args[0],int):
            raise StoneException("pop index must be an integer")
        index=args[0]
        if index<0 or index>=len(self.value):
            raise StoneException("pop index out of range")
        return self.value.pop(index)
    def getValueByIndex(self,index):
        return self.value[index]
    def setValueByIndex(self,index,value):
        self.value[index]=value
        return value

        

