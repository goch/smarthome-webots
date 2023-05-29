from SHDevices.sh_motionsensor import *

class SH_SNZB_03_motion_sensor(SH_MotionSensor):

    def __init__(self,name, connection=None, device=None, states={}, fields={}):
        super().__init__(name, connection, device, states, fields)        

        # add Devices
        # self.motor_position = device.getDevice("position sensor")
        # self.motor_position.enable(device.getBasicTimeStep())

        # add states
        super().add_state('battery', description='Battery percent', value=95, unit='%')
        super().add_state('voltage', description='Battery voltage',value=3.2, unit='V')
        super().add_state('no_motion', description='Time from last motion',value=0, unit='s')
        super().add_state('occupancy', description='Occupancy',value=False)
        
        # remap states
        super().remapState('last_motion','no_motion')
        super().remapState('motion_detected','occupancy')

        super().ignoreState('targets')

    
    # get Transform from Device
    def getTransform(self):
        return self.getFieldValue("translation")
    
    def update(self, step):
        self.deltaTime +=step
        super().update(step)
        pass

    # message received
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
                self.log("resolve Remap for state: " + name)
                super().setState(self.resolveRemap(name), value)
                pass
    
    def register(self):
        super().register()

    def reset(self):
        super().reset()
        self.sendReset()
        pass