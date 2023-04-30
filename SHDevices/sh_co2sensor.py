from SHDevices.sh_device import *
from math import sqrt, pow

class SH_CO2Sensor(SHDevice):

    def __init__(self,name, connection=None, device=None, states={}, fields={}):
        super().__init__(name, connection, device, states, fields)        

        self.deltaTime = 0

        self.sensor_range = 3.3
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

    def getDistance(self,x1,y1,x2,y2):
        # self.log(str(sqrt( pow((x1 - x2),2) + pow((y1 - y2),2))))
        return sqrt( pow((x1 - x2),2) + pow((y1 - y2),2))


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

    def update(self, step):
        self.deltaTime +=step

    # measure data every 10seconds
        if self.deltaTime > 10000:
            self.deltaTime = 0    

            # check if WINDOW send OPEN/CLOSE
            if self.receiver.getQueueLength() > 0:
                msg = self.receiver.getFloats()
                sensor_pos = self.getTransform()
                
                # check if window is open
                if self.getDistance(sensor_pos[0],sensor_pos[1],msg[1],msg[2]) < self.sensor_range:
                    if bool(msg[0]) == True:
                        self.window_open_count +=1
                    elif self.window_open_count > 0:
                        self.window_open_count -=1
                    
                    self.receiver.nextPacket()

            humans = self.device.getFromDef("HUMAN")
            # human_name = humans.getField("name").getSFString()
            
            co2_level = self.getCO2Concentration()
            # there is a human
            if humans is not None:
                human_pos = humans.getField("translation").getSFVec3f()
                sensor_pos = self.getTransform()
                # sh_device.log(human_name + "-> " + str(human_pos))
                # sh_device.log(str(sensor_pos))
                        
                distance = self.getDistance(sensor_pos[0],sensor_pos[1], human_pos[0],human_pos[1])

                # if human in range increase co2
                if distance <= self.sensor_range:
                    co2_level += 10
                pass    
    
            # decrease co2 if windows open     
            co2_level -= 10 * self.window_open_count               
            self.updateCO2Concentration(co2_level)  

            pass

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