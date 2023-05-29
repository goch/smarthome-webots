from SHDevices.sh_device import *

class SH_MotionSensor(SHDevice):

    def __init__(self,name, connection=None, device=None, states={}, fields={}):
        super().__init__(name, connection, device, states, fields)        

        self.deltaTime = 0
        self.lastMotionTime = 0    

        self.radar = device.getDevice("radar")
        self.radar.enable(64)

        self.motionDetected = False

        # add states
        super().add_state(name='targets',value=0,description="Number of moving objects detected")
        super().add_state(name='motion_detected',value=False, description="Motion detected")
        super().add_state(name='last_motion',value=0, description="Seconds since last motion detected", unit="s")
        # super().add_state('speed',0.0)
        # super().add_state('distance',0.0)
        # super().add_state('angle',0.0)


        # add fields
        super().add_field('last_motion_intervall',self.device.getSelf().getField("last_motion_intervall"))
        super().add_field('last_motion_begin',self.device.getSelf().getField("last_motion_begin"))

        
        self.last_motion_intervall = self.getFieldValue('last_motion_intervall') * 1000 
        self.last_motion_begin = self.getFieldValue('last_motion_begin') * 1000
        
        

    def setNumberOfTargets(self,number):
        if number != self.getStateValue('targets'):
            self.setStateValue('targets', number)
        pass

    def getMotionDetected(self):
        target_count = self.radar.getNumberOfTargets()
        self.setNumberOfTargets(target_count)
        motion_detected = any(target.speed != 0 for target in self.getTargets())
        
        if motion_detected != self.motionDetected:
            self.setStateValue('motion_detected', motion_detected)
            self.motionDetected = motion_detected

        return motion_detected

    def getTargets(self):
        return self.radar.getTargets()

    def update(self, step):
        self.deltaTime += step
        self.lastMotionTime += step

        if self.deltaTime > 500:
            motion = self.getMotionDetected()
            if motion:
                self.setStateValue('last_motion', 0)
                self.lastMotionTime = 0
            self.deltaTime = 0

        if self.lastMotionTime >= self.last_motion_begin:
            last_motion = self.getStateValue('last_motion') 
            if last_motion == 0:
                self.setStateValue('last_motion', self.last_motion_begin / 1000)
            elif self.lastMotionTime % self.last_motion_intervall == 0:
                self.setStateValue('last_motion', last_motion + self.last_motion_intervall / 1000) 
        pass


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