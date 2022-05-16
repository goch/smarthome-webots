import json
class SH_State(object):

    def __init__(self, name, value, dataType=None, min=None, max=None, read=True, write=True ):
        self.name = name
        self.min = min
        self.max = max
        self.value = value
        self.read = read
        self.write = write
        self.setType(dataType)
    
    def getName(self):
        return self.name

    def setName(self,name):
        self.min = name
    
    def getMin(self):
        return self.min

    def setMin(self,min):
        self.min = min
    
    def getMax(self):
        return self.max

    def setMax(self,max):
        self.max = max

    def getValue(self):
        return self.value

    def setValue(self,value):
        if self.min is not None and value < self.min:
            value = self.min
        elif self.max is not None and value > self.max:
            value = self.max

        self.value = value

    def getRead(self):
        return self.read
    
    def setRead(self,value):
        self.read = value

    def getWrite(self):
        return self.write
    
    def setWrite(self,value):
        self.write = value

    def getType(self):
        return self.dataType

    def setType(self,value):
        if value == None:
            self.dataType = str(type(self.getValue()))
        else: 
            self.dataType = value 

    def toDict(self,full=True):
        data = {}
        data['name'] = self.getName()
        data['value'] = self.getValue()
        
        if full:
            data['min'] = self.getMin()
            data['max'] = self.getMax()
            data['read'] = self.getRead()
            data['write'] = self.getWrite()
            data['type'] = self.getType()

        return data
