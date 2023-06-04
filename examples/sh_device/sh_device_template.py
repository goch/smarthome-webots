from SHDevices.sh_device import *

class SH_Template(SHDevice):

    def __init__(self,name, connection=None, device=None, states={}, fields={}):
        super().__init__(name, connection, device, states, fields)        

        self.deltaTime = 0
        # add Devices
        # self.motor_position = device.getDevice("position sensor")
        # self.motor_position.enable(int(device.getBasicTimeStep()))

        # add states
        # super().add_state(name='battery',value=99, description="Battery percent", min=0, max=100, unit='%')

        # add fields
        #super().add_field('translation', self.getField("translation"))

        # remap states
        #super().remapState('currentTemperature','temperature')

    
    # get Transform from Device
    def getTransform(self):
        return self.getFieldValue("translation")
    
    def update(self, step):
        self.deltaTime +=step
        super().update(step)
        pass

    # state message received
    def setState(self, name, value):    

        match name:
            case "battery":
                # self.setPosition(value)
                pass
            case "up":
                # self.setUp(value)
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