from SHDevices.sh_device import *

class SH_Alarm(SHDevice):

    def __init__(self,name, connection=None, device=None, states={}, fields={}):
        super().__init__(name, connection, device, states, fields)        

        self.deltaTime = 0
        # add Devices
        self.sensor = device.getDevice("distance sensor")
        self.sensor.enable(64)
        self.triggered = False

        # add states
        super().add_state('armed',False)
        super().add_state('armed_distance',0.0)
        super().add_state('triggered',False)
        super().add_state('on',False)
        super().add_state('brightness',4.0)
        

        self.alarm_lamp = device.getSelf()

        # add fields
        super().add_field('on', self.alarm_lamp.getField("on"))
        super().add_field('brightness', self.alarm_lamp.getField("brightness"))
        super().add_field('location', self.alarm_lamp.getField("lightLocation"))

        self.fields['brightness'].setSFFloat(4.0)
        self.fields['on'].setSFBool(False)
        
    
    def setTriggered(self, triggered):
        if self.getStateValue('triggered') != triggered and self.getStateValue('armed'):
            self.log("triggered -> " + str(triggered))
            self.setStateValue('triggered', triggered)
            self.setOn(True)

    def getTriggered(self):
        return self.getStateValue('triggered')
        
    def getDistance(self):
        return self.sensor.getValue()

    def getArmedDistance(self):
        return self.getStateValue('armed_distance') 
    
    def setArmedDistance(self, distance):
        self.setStateValue('armed_distance', distance)

    def getTriggerDistance():
        return 

    def getArmed(self):
        return self.getStateValue('armed')
    
    def setArmed(self, armed):
        self.setStateValue('armed', armed)
        if armed:
            self.setArmedDistance(self.getDistance())
        else: 
            self.setArmedDistance(0)
            self.setOn(False)
            self.setStateValue('triggered', False)

    def setOn(self,on):
        self.fields['on'].setSFBool(on)
        self.setStateValue('on', on)

    def getOn(self):
        return self.getStateValue('on')

    def setBrightness(self, value):
        self.fields['brightness'].setSFFloat(value)
        if value == 0:
            self.setStateValue('on', False)
            self.setStateValue('brightness', 0)
        pass

    def update(self, step):
        self.deltaTime +=step

        if self.deltaTime > 1000:
            self.deltaTime = 0
    
            if self.getArmed() and self.getTriggered():
                self.setOn( not self.getOn())

            if self.getDistance() != self.getArmedDistance():
                self.setTriggered(True)
            else: 
                self.setTriggered(False)

        pass

    def setState(self, name, value):    

        match name:
            case "trigger":
                self.setTriggered(value)
                pass
            case "armed":
                self.setArmed(value)
                pass
            case "on":
                self.setOn(value)
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