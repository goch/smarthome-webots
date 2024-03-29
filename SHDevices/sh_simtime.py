from cmath import pi
from datetime import datetime
from SHDevices.sh_device import *

class SH_SimTime(SHDevice):

    def __init__(self,name, connection=None, device=None, states={}, fields={}, hour=0, minute=0, second=0):
        super().__init__(name, connection, device, states, fields)        

        self.deltaTime = 0

        # add Devices
        self.hour_motor = device.getDevice("hour motor")
        self.minute_motor = device.getDevice("minute motor")
        self.second_motor = device.getDevice("second motor")

        self.second_step = 2 * pi / 60
        self.minute_step = 2 * pi / 60
        self.hour_step = 2 * pi / 12

        # add states
        super().add_state('timestamp',0.0)
        super().add_state('hour',hour)
        super().add_state('minute',minute)
        super().add_state('second',second)

        # add fields
        #super().add_field('position',device.getField("pointLightColor"))
    # 


    def setTimeStamp(self,value):
        self.setStateValue('timestamp', value)
        pass

    def updateTimeStamp(self):
        today = datetime.today()
        simtime = today.replace(hour=int(self.getHour()), minute=int(self.getMinute()), second=int(self.getSecond()))
        
        self.setTimeStamp( datetime.timestamp(simtime) )


    def setHour(self,value):
        self.setStateValue('hour', value % 12)
        pass

    def setMinute(self,value):
        self.setStateValue('minute', value % 60)
        pass

    def setSecond(self,value):
        self.setStateValue('second', value % 60)
        pass

    def getHour(self):
        return self.getStateValue('hour')

    def getMinute(self):
        return self.getStateValue('minute')

    def getSecond(self):
        return self.getStateValue('second')

    def getTimeStamp(self):
        return self.getStateValue('timestamp')

    def updateClock(self, deltatime):
        deltaSeconds = (deltatime/1000)

        self.setSecond( self.getSecond() + (deltaSeconds))
        self.setMinute( self.getMinute() + (deltaSeconds / 60) )
        self.setHour( self.getHour() + (deltaSeconds / 3600) )

        self.updateTimeStamp()
        
        hour12 = self.getHour() - 12
        if hour12 < 0:
            hour12 = self.getHour()

        self.second_motor.setPosition( self.getSecond() * self.second_step) 
        self.minute_motor.setPosition( self.getMinute() * self.minute_step)
        self.hour_motor.setPosition( hour12 * self.hour_step)
        pass

    def update(self, step):
        self.deltaTime +=step
        # do something every 1000ms
        if self.deltaTime > 1000:
            self.updateClock(self.deltaTime)
            self.deltaTime = 0
        pass

    def setState(self, name, value):    

        match name:
            case "timestamp":
                # self.setPosition(value)
                pass
            case "hour":
                # self.setUp(value)
                pass
            case "minute":
                # self.setDown(value)
                pass
            case "second":
                # self.setStop(value)
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