from SHDevices.sh_device import *


class SH_Shutter(SHDevice):

    def __init__(self,name, connection=None, device=None, states={}, fields={}):
        super().__init__(name, connection, device, states, fields)        

        self.motor = device.getDevice("linear motor")
        self.motor.setPosition(self.motor.getMaxPosition())
        self.motor_position = device.getDevice("position sensor")
        self.motor_position.enable(64)

        self.emitter = device.getDevice("emitter")

        self.window_open = False

        super().add_state('setPosition',self.motor.getMaxPosition())
        super().add_state('up',False)
        super().add_state('down',False)
        super().add_state('stop',True)
        super().add_state('currentPosition',self.motor.getMaxPosition())

        #super().add_field('position',device.getField("pointLightColor"))
        #super().add_field('velocity',device.getField("pointLightColor"))

        
    
        # self.reset()

    def setPosition(self,target_position):
        self.log("setPosition: " + str(target_position))
        self.setStateValue('setPosition', target_position)
        self.motor.setPosition(target_position)
        
        self.setStateValue('stop', False)
        if self.motor_position.getValue() < target_position:
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

    def setDown(self, down):
        if down:
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
            self.setPosition(self.motor.getMaxPosition())
        else:
            self.setStateValue('up', False)
            self.setStop(True)
    
    def setStop(self,stop):
        if stop:
            self.setPosition(self.motor_position.getValue())
            self.setStateValue('stop', True)

    def updateCurrentPosition(self,position):
        self.setStateValue('currentPosition', position)
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
            
