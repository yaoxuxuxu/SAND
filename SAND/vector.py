from .StoneException import StoneException
class Vector:
    def __init__(self,value:list=[]):
        self.value=value
    def __len__(self):
        return len(self.value)
    def __str__(self):
        return str(self.value)
    def __eq__(self, other):
        if not isinstance(other,Vector):
            return False
        if len(other)!=len(self):
            return False
        for i in range(len(self)):
            if self.value[i]!=other.value[i]:
                return False
        return True
    def fetch_method(self,name):
        try:
            method=getattr(self,name)
        except:
            raise StoneException("No method called"+name)
        return method
    def append(self,element):
        self.value.append(element)
    def length(self):
        return len(self.value)
    def pop(self,index):
        if not isinstance(index,int):
            raise StoneException("pop index must be an integer")
        if index<0 or index>=len(self.value):
            raise StoneException("pop index out of range")
        return self.value.pop(index)
    def getValueByIndex(self,index):
        return self.value[index]
    def setValueByIndex(self,index,value):
        self.value[index]=value
        return value

        

