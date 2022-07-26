from SHDevices.sh_device import *


class SH_Shutter(SHDevice):

    def __init__(self,name, connection=None, device=None, states={}, fields={}):
        super().__init__(name, connection, device, states, fields)        

        self.deltaTime = 0

        self.motor = device.getDevice("linear motor")
        self.motor.setPosition(self.motor.getMaxPosition())
        self.motor_position = device.getDevice("position sensor")
        self.motor_position.enable(64)

        self.emitter = device.getDevice("emitter")
        self.finalPositionReached = False
        self.window_open = False

        super().add_state('setPosition',self.motor.getMaxPosition())
        super().add_state('currentPosition',self.motor.getMinPosition())
        super().add_state('up',False)
        super().add_state('down',False)
        super().add_state('stop',True)


        super().add_field('transparency',self.device.getSelf().getField("ShutterTransparency"))
        #super().add_field('velocity',device.getField("pointLightColor"))
        self.setShutterTransparency(0.0)
        
    
        # self.reset()
    def setShutterTransparency(self, transparency):
        self.fields['transparency'].setSFFloat(transparency)

    def setPosition(self,target_position):
        self.log("setPosition: " + str(target_position))
        self.setStateValue('setPosition', target_position)
        self.motor.setPosition(target_position)
        
        self.setStateValue('stop', False)
        if self.getPosition() < target_position:
              self.setStateValue('up',True)
              self.setStateValue('down', False)
              self.motor.setPosition(target_position)
        elif self.motor_position.getValue() > target_position:
            self.setStateValue('down', True)
            self.setStateValue('up', False)
            self.motor.setPosition(target_position)
        else:
            self.setStateValue('stop', True)
            self.setStateValue('down', False)
            self.setStateValue('up', False)
    
    def getPosition(self):
        return self.motor_position.getValue()

    def setDown(self, down):
        if down:
            self.setShutterTransparency(0.0)
            self.finalPositionReached = False
            self.setPosition(self.motor.getMinPosition())
        else:
            self.setStateValue('down', False)
            self.setStop(True)

    def emitt(self,state):
        if self.window_open != state:
            self.window_open = state
            self.log("Emitting ->" + str(state))
            tf = self.device.getSelf().getField("translation").getSFVec3f() 
            msg = struct.pack("?ddd",state,tf[0],tf[1],tf[2])
            self.emitter.send(msg)
        
    def setUp(self, up):
        if up:
            self.setShutterTransparency(0.0)
            self.finalPositionReached = False
            self.setPosition(self.motor.getMaxPosition())
        else:
            self.setStateValue('up', False)
            self.setStop(True)
    
    def setStop(self,stop):
        if stop:
            self.setPosition(self.getPosition())
            self.updateCurrentPosition()
            self.setStateValue('stop', True)
            self.setStateValue('up', False)
            self.setStateValue('down', False)


    def updateCurrentPosition(self):

        targetPosition = self.getStateValue('setPosition')
        currentPosition = self.getStateValue('currentPosition')

        if targetPosition != currentPosition:
            self.setStateValue('currentPosition', self.motor_position.getValue())
        elif  not self.finalPositionReached:
            self.finalPositionReached = True
            self.setStateValue('currentPosition', self.motor_position.getValue())
            self.setStop(True)
        elif currentPosition == self.motor.getMaxPosition():
            self.setShutterTransparency(0.7)

        pass
    
    def update(self, step):
        self.deltaTime +=step
        # TODO ALSO UPDATE CURRENT POSITION IF TARGET POSITION REACHED
        # do something every 1000ms
        if self.deltaTime > 1000: 
            self.updateCurrentPosition()
            self.deltaTime = 0
        pass

    def setState(self, name, value):

        match name:
            case "setPosition":
                self.setPosition(value)
            case "up":
                self.setUp(value)
            case "down":
                self.setDown(value)
            case "stop":
                self.setStop(value)
            case _:
                self.log("state not found or state is read only. Value ->" + str(value))

    
    def register(self):
        super().register()

    def reset(self):
        super().reset()
        self.sendReset()
        pass
            
