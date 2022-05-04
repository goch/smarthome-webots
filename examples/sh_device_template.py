from SHDevices.sh_device import *

class SH_Shutter(SHDevice):

    def __init__(self,name, connection=None, device=None, states={}, fields={}):
        super().__init__(name, connection, device, states, fields)        
                
        # add states
        # super().add_state('setPosition',1.3)

        # add fields
        #super().add_field('position',device.getField("pointLightColor"))


        self.reset()    

    # 
    def setState(self, name, value):    
        super().setState(name, value)

        match name:
            case "setPosition":
                # self.setPosition(value)
                pass
            case "up":
                # self.setUp(value)
                pass
            case "down":
                # self.setDown(value)
                pass
            case "stop":
                # self.setStop(value)
                pass
            case _:
                print("state not found or state is read only")
                pass

        self.send(self.toJSON())
    
    def register(self):
        super().register()
        self.send(self.toJSON())


    def reset(self):
        # self.set_state('setPosition',1.3)
        pass