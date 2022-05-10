from SHDevices.sh_device import *

class SH_Distance_Sensor(SHDevice):

    def __init__(self,name, connection=None, device=None, states={}, fields={}):
        super().__init__(name, connection, device, states, fields)        
                

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
        return self.states["trigger_distance"]
        
    def getDistance(self):
        return self.sensor.getValue()

    def setTriggered(self, triggered):
        if self.triggered != triggered:
            self.triggered = triggered
            self.log("triggered -> " + str(triggered))
            self.states["triggered"] = triggered
            self.send(self.toJSON())

    def updateCurrentDistance(self):
        self.states['distance'] = self.sensor.getValue()
        self.send(self.toJSON())

        
    def setState(self, name, value):    
        super().setState(name, value)

        match name:
            case "trigger_distance":
                self.states[name] = value
                pass
            case "distance":
                self.states[name] = value
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