from SHDevices.sh_device import *

class SH_CO2_Sensor(SHDevice):

    def __init__(self,name, connection=None, device=None, states={}, fields={}):
        super().__init__(name, connection, device, states, fields)        


        self.sensor_range = 3
        self.threshholds = device.getSelf().getField('threshholds').getSFVec3f()
        self.window_open_count = 0
        # add Devices
        self.receiver = device.getDevice("receiver")
        self.receiver.enable(int(device.getBasicTimeStep()))
        
        # add states
        super().add_state('co2_concentration',800, min=500, max=5000)
        super().add_state('air_quality','GOOD')

        # add fields
        #super().add_field('position',device.getField("pointLightColor"))
    

    def getTransform(self):
        return self.device.getSelf().getField("translation").getSFVec3f()

    def updateCO2Concentration(self,value):
        self.setCO2Concentration(value)
        set_value = self.getCO2Concentration()

        if set_value < self.threshholds[0]:            
            self.setAirQuality("GOOD")
        elif set_value < self.threshholds[1]:
            self.setAirQuality("BAD")
        else:
            self.setAirQuality("CRITICAL")


    def getCO2Concentration(self):
        return self.getStateValue('co2_concentration')

    def setCO2Concentration(self,value):
        self.setStateValue('co2_concentration', value, ignoreSame=True)

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