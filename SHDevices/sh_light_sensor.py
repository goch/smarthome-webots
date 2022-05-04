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

        self.reset()    

    def updateLuminosity(self,value):
        self.log("new Luminosity -> " + str(value))
        self.states['luminosity'] = value
        self.send(self.toJSON())

    def setState(self, name, value):    
        super().setState(name, value)

        match name:
            case "luminosity":
                # read only value
                pass
            case _:
                print("state not found or state is read only")
                pass

        self.send(self.toJSON())
    
    def register(self):
        super().register()
        self.connection.send(self.toJSON())


    def reset(self):
        # self.set_state('setPosition',1.3)
        pass