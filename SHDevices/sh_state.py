import json
class SH_State(object):

    def __init__(self, name, value, unit="", description="", dataType=None, min=None, max=None, read=True, write=True):
        self.name = name
        self.description = description
        self.min = min
        self.max = max
        self.value = value
        self.unit = unit
        self.read = read
        self.write = write
        self.setType(dataType)

        self.remap = None

    def getName(self):
        if self.remap is not None:
            return self.remap
        else:
            return self.name

    def setName(self,name):
        self.min = name
    
    def getDescription(self):
        return self.description

    def getUnit(self):
        return self.unit

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

    def setRemap(self,remap):
        self.remap = remap

    def is_remapped(self):
        return self.remap is not None

    def toDict(self,full=True):
        data = {}
        data['name'] = self.getName()
        data['value'] = self.getValue()
        
        if full:
            data['description'] = self.getDescription()
            data['min'] = self.getMin()
            data['max'] = self.getMax()
            data['unit'] = self.getUnit()
            data['read'] = self.getRead()
            data['write'] = self.getWrite()
            data['type'] = self.getType()

        return data
