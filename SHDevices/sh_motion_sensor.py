from SHDevices.sh_device import *

class SH_Motion_Sensor(SHDevice):

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
        if number != self.states["targets"]:
            self.states["targets"] = number
            self.send(self.toJSON())
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
            self.states["motion_detected"] = motion_detected
            self.motionDetected = motion_detected
            self.send(self.toJSON())

        return motion_detected

    def getTargets(self):
        return self.radar.getTargets()

    def setState(self, name, value):    
        super().setState(name, value)

        match name:
            case "setPosition":
                # self.setPosition(value)
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