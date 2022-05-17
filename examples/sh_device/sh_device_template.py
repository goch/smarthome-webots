from SHDevices.sh_device import *

class SH_Template(SHDevice):

    def __init__(self,name, connection=None, device=None, states={}, fields={}):
        super().__init__(name, connection, device, states, fields)        

        # add Devices
        # self.motor_position = device.getDevice("position sensor")
        # self.motor_position.enable(64)


        # add states
        # super().add_state('setPosition',1.3)

        # add fields
        #super().add_field('position',device.getField("pointLightColor"))
    # 
    def setState(self, name, value):    

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
    
    def register(self):
        super().register()

    def reset(self):
        super().reset()
        self.sendReset()
        pass