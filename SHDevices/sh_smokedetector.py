from SHDevices.sh_device import *
from math import sqrt, pow


class SH_SmokeDetector(SHDevice):

    def __init__(self,name, connection=None, device=None, states={}, fields={}):
        super().__init__(name, connection, device, states, fields)        

        self.deltaTime = 0
        # add Devices
        self.receiver = device.getDevice("receiver")
        self.receiver.enable(int(device.getBasicTimeStep()))

        self.sensor_range = 3
        self.test_duration = 500
        self.current_test_duration = 0

        # add states
        super().add_state('triggered',False)
        super().add_state('batteryCapacity',0.5, min=0.0, max=1.0)
        super().add_state('test',False)


        # add fields
        #super().add_field('position',device.getField("pointLightColor"))
    
    def getTransform(self):
        return self.device.getSelf().getField("translation").getSFVec3f()

    def update(self, step):
        self.deltaTime +=step
            # measure data every 10s
        if self.deltaTime > 10000:
            self.deltaTime = 0
            
            if self.checkFire():
                self.triggerAlarm()
            #fires = sh_device.device.getFromDef("FIRE")
            # human_name = humans.getField("name").getSFString()

            if self.getTest():
                self.runTest(step)

            self.drainBattery(step)
        pass

    def setState(self, name, value):    

        match name:
            case "test":
                self.setTest(value)
                pass
            case "triggered":
                self.setTriggered(value)
                pass
            case "batteryCapacity":
                self.setBatteryCapacity(value)
                pass
            case _:
                print("state not found or state is read only")
                pass


    def checkFire(self):
        # check if Fire in Range
        if self.receiver.getQueueLength() > 0:
            msg = self.receiver.getData()
            data = struct.unpack("?ddd",msg)
            self.log(str(data))
        
            sensor_pos = self.getTransform()
            
            # check if fire found
            if self.getDistance(sensor_pos[0],sensor_pos[1],data[1],data[2]) < self.sensor_range:
                self.log(str(data[0]))
                
                self.receiver.nextPacket()
            
            return data[0]
        
        return False

        

    def isTriggered(self):
        return self.getStateValue('triggered')

    def setTriggered(self,value):
        self.setStateValue('triggered', value) 

    def getTest(self):
        return self.getStateValue('test')

    def runTest(self, deltaTime):
        self.current_test_duration += deltaTime 
        if self.current_test_duration <= self.test_duration:
            # enable LED
            # enable Siren
            pass
        else:
            self.current_test_duration = 0
            self.setTest(False)

    def triggerAlarm(self):
        pass

    def getBatteryCapacity(self):
        return self.getStateValue('batteryCapacity')

    def setBatteryCapacity(self,value):
        self.setStateValue('batteryCapacity', value)

    def drainBattery(self, deltaTime):
        pass

    def getDistance(x1,y1,x2,y2):
        return sqrt( pow((x1 - x2),2) + pow((y1 - y2),2))


    def setTest(self,value):
        self.setStateValue('test', value)
    
    def register(self):
        super().register()

    def reset(self):
        super().reset()
        self.sendReset()
        pass