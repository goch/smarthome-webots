from SHDevices.sh_device import *

class SH_IKEA_tradfri_dimmer_switch_E1734(SHDevice):

    def __init__(self,name, connection=None, device=None, states={}, fields={}):
        super().__init__(name, connection, device, states, fields)        

        # add Devices
        # self.motor_position = device.getDevice("position sensor")
        # self.motor_position.enable(device.getBasicTimeStep())

        # add states
        super().add_state(name='available',value=True,description="Available")
        # super().add_state(name='battery',value=87,description="Battery percent", unit='%')
        super().add_state(name='down_button',value=False, description="Down Button Pressed")
        super().add_state(name='up_button',value=False, description="Up Button Pressed")
        # super().add_state(name='link_quality',value=255, description="Link Quality", min=0, max=255)
        super().add_state(name='state',value=False, description="Switch Event",)

        # add fields
        #super().add_field('position',device.getField("pointLightColor"))
    
    # get Transform from Device
    def getTransform(self):
        return self.device.getSelf().getField("translation").getSFVec3f()
    
    # message received
    def setState(self, name, value):    
        self.setStateValue(name,value)
        match name:
            case "available":
                # self.setPosition(value)
                pass
            case "down_button":
                # self.setUp(value)
                pass
            case "up_button":
                # self.setDown(value)
                pass
            case "state":
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