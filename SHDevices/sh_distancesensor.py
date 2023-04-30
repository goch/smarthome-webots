from SHDevices.sh_device import *

class SH_DistanceSensor(SHDevice):

    def __init__(self,name, connection=None, device=None, states={}, fields={}):
        super().__init__(name, connection, device, states, fields)        
                
        self.deltaTime = 0

        self.sensor = device.getDevice("distance sensor")
        self.sensor.enable(64)
        self.triggered = False


        # add states
        super().add_state('distance',0.0)
        super().add_state('triggered',True)
        super().add_state('trigger_distance', 0.1)
        super().add_state('max_distance', self.sensor.getMaxValue())
        super().add_state('min_distance', self.sensor.getMinValue())
        

        # add fields
        #super().add_field('position',device.getField("pointLightColor"))
    # 

    def getTriggerDistance(self):
        return self.getStateValue('trigger_distance')
        
    def getDistance(self):
        return self.getStateValue('distance')

    def setDistance(self,value):
        self.setStateValue('distance', value)

    def setTriggered(self, triggered):
        if self.triggered != triggered:
            self.triggered = triggered
            self.log("triggered -> " + str(triggered))
            self.setStateValue('triggered', triggered) 


    def updateCurrentDistance(self):
        distance = self.sensor.getValue()
        self.log(distance)
        if self.getDistance() != distance:
            self.setDistance(distance)
        
    def update(self, step):
        self.deltaTime +=step
        # do something every 500ms
        if self.deltaTime > 500:
            self.deltaTime = 0
            self.updateCurrentDistance()

            if self.getDistance() <= self.getTriggerDistance():
                self.setTriggered(True)
            else:
                self.setTriggered(False)
        pass
    
    def setState(self, name, value):    

        match name:
            case "trigger_distance":
                self.setStateValue(name, value)
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