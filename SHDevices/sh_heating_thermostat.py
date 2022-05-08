from SHDevices.sh_device import *

class SH_Heating_Thermostat(SHDevice):

    def __init__(self,name, connection=None, device=None, states={}, fields={}):
        super().__init__(name, connection, device, states, fields)        
                
        # add states
        super().add_state('setTemperature',21.0)
        super().add_state('currentTemperature',19.0)
        # add fields
        #super().add_field('position',device.getField("pointLightColor"))


        # self.reset()    

    
    def setTemperature(self,value):
        self.states['setTemperature'] = value    

    def getSetTemperature(self):
        return self.states['setTemperature']
    
    def getCurrentTemperature(self):
        return self.states['currentTemperature']


    def updateCurrentTemperature(self,temperature):
        self.log("Update Temperature: " + str(temperature) + "/" + str(self.getSetTemperature()))
        self.states['currentTemperature'] = temperature
        self.send(self.toJSON())
        pass

    def setState(self, name, value):    
        super().setState(name, value)

        match name:
            case "setTemperature":
                self.setTemperature(value)
                pass
            case _:
                print("state not found or state is read only")
                pass

        self.send(self.toJSON())
    
    def register(self):
        super().register()
        self.send(self.toJSON())


    def reset(self):
        super().reset()
        # self.set_state('setPosition',1.3)
        self.send(self.toJSON())
        pass