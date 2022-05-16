from SHDevices.sh_device import *

class SH_CO2_Sensor(SHDevice):

    def __init__(self,name, connection=None, device=None, states={}, fields={}):
        super().__init__(name, connection, device, states, fields)        


        self.sensor_range = 3
        self.threshholds = [1000,1500,2000]
        self.min = 500
        self.max = 5000

        # add Devices
        # self.motor_position = device.getDevice("position sensor")
        # self.motor_position.enable(64)
        
        # add states
        super().add_state('co2_concentration',800)
        super().add_state('air_quality','GOOD')

        # add fields
        #super().add_field('position',device.getField("pointLightColor"))
    

    def getTransform(self):
        return self.device.getSelf().getField("translation").getSFVec3f()

    def updateCO2Concentration(self,value):
        # TODO MOVE to min max of State Class
        if value < self.min:
            value = self.min
        elif value > self.max:
            value = self.max

        if value < self.threshholds[0]:            
            self.setAirQuality("GOOD")
        elif value < self.threshholds[1]:
            self.setAirQuality("BAD")
        else:
            self.setAirQuality("CRITICAL")

        if value != self.getCO2Concentration():
            self.log(self.getAirQuality() + " CO2 concentration -> " + str(value) + "ppm")
            self.setCO2Concentration(value)

    def getCO2Concentration(self):
        return self.getStateValue('co2_concentration')

    def setCO2Concentration(self,value):
        self.setStateValue('co2_concentration', value)

    def setAirQuality(self,value):
        self.setStateValue('air_quality',value)

    def getAirQuality(self):
        return self.getStateValue('air_quality')

    def setState(self, name, value):    

        match name:
            case "co2_concentration":
                self.setCO2Concentration(value)
                pass
            case _:
                print("state not found or state is read only")
                pass
    
    def register(self):
        super().register()

    def reset(self):
        super().reset()
        # self.set_state('setPosition',1.3)
        self.sendReset()
        pass