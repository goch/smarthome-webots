from SHDevices.sh_thermostat import *

class SH_SNZB_02_temperature_humidity(SH_Thermostat):

    def __init__(self,name, connection=None, device=None, states={}, fields={}):
        super().__init__(name, connection, device, states, fields)        

        super().add_state('battery', description='Battery percent', value=100, unit='%')
        super().add_state('voltage', description='Battery voltage',value=3.4, unit='V')
        super().add_state('temperature', description='Temperature',value=19, unit='°C')
        super().add_state('humidity', description='Humidity',value=40, unit='%')
        

        super().remapState('currentTemperature','temperature')
        super().remapState('currentHumidity','humidity')

        self.timediff = 0

    # get Transform from Device
    def getTransform(self):
        return self.device.getSelf().getField("translation").getSFVec3f()
    

    def update(self, step): 
        super().update(step)
        pass


    # message received
    def setState(self, name, value):    

        match name:
            case "battery":
                self.setStateValue(name,value)
                pass
            case "voltage":
                self.setStateValue(name,value)
                pass                
            case _:
                self.log("resolve Remap for state: " + name)
                super().setState(self.resolveRemap(name), value)
                pass
    
    def register(self):
        super().register()

    def reset(self):
        super().reset()
        self.sendReset()
        pass