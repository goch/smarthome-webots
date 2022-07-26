from SHDevices.sh_device import *

class SH_MotionSensor(SHDevice):

    def __init__(self,name, connection=None, device=None, states={}, fields={}):
        super().__init__(name, connection, device, states, fields)        
                

        self.radar = device.getDevice("radar")
        self.radar.enable(64)

        self.motionDetected = False

        # add states
        super().add_state('targets',0)
        super().add_state('motion_detected',False)
        # super().add_state('speed',0.0)
        # super().add_state('distance',0.0)
        # super().add_state('angle',0.0)


        # add fields
        #super().add_field('position',device.getField("pointLightColor"))
    # 

    def setNumberOfTargets(self,number):
        if number != self.getStateValue('targets'):
            self.setStateValue('targets', number)
        pass

    def getMotionDetected(self):

        motion_detected = False
        target_count = self.radar.getNumberOfTargets()
        self.setNumberOfTargets(target_count)
        if  target_count > 0:
            targets = self.getTargets()

            for target in targets:
                if target.speed != 0:
                    motion_detected = True
                    break
        else:
            motion_detected = False
            
        if motion_detected != self.motionDetected:
            self.setStateValue('motion_detected', motion_detected)
            self.motionDetected = motion_detected

        return motion_detected

    def getTargets(self):
        return self.radar.getTargets()

    def setState(self, name, value):    

        match name:
            case "setPosition":
                # self.setPosition(value)
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