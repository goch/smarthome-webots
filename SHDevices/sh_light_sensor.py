from SHDevices.sh_device import *

class SH_Light_Sensor(SHDevice):

    def __init__(self,name, connection=None, device=None, states={}, fields={}):
        super().__init__(name, connection, device, states, fields)        
                
        # add states
        super().add_state('luminosity',0)

        # add fields
        #super().add_field('position',device.getField("pointLightColor"))

        self.sensor = device.getDevice("light sensor")
        self.sensor.enable(64)

        # self.reset()    

    def updateLuminosity(self):
        self.setStateValue('luminosity', self.sensor.getValue(), ignoreSame=False)

    def setState(self, name, value):    

        match name:
            case "luminosity":
                # read only value
                pass
            case _:
                print("state not found or state is read only")
                pass
    
    def register(self):
        super().register()


    def reset(self):
        super().reset()
        self.sendReset()
        pass