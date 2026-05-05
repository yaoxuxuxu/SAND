class Vector:
    def __init__(self,value:list=[]):
        self.value=value
    def __len__(self):
        return len(self.value)
    def getValueByIndex(self,index):
        return self.value[index]
    def setValueByIndex(self,index,value):
        self.value[index]=value
        return value

        

