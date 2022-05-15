from SHDevices.sh_device import *

class SH_Power_Plug(SHDevice):

    def __init__(self,name, connection=None, device=None, states={}, fields={}):
        super().__init__(name, connection, device, states, fields)        

        # add Devices
        self.led = device.getDevice("led")
        self.connector = device.getDevice("connector")


        # add states
        super().add_state('on',False)
        super().add_state('currentPowerConsumption',0.0)
        super().add_state('energyCounter',0.0)
        super().add_state('resetEnergyCounter',False)

        # add fields
        #super().add_field('position',device.getField("pointLightColor"))
    # 

    def turnOn(self,state):
        self.setLED(state)
        self.states["on"] = state
        if state:
            self.setCurrentPower(9000)
        else:
            self.setCurrentPower(0)
        pass

    def setLED(self,state):
        self.led.set(int(state))

    def setCurrentPower(self,value):
        self.states["currentPowerConsumption"] = value
    
    def getCurrentPower(self):
        return self.states["currentPowerConsumption"]

    def addEnergyCounter(self,value):
        self.states['energyCounter'] += value
        self.send(self.toJSON())


    def updateEnergyCounter(self, deltaTime):
        currentPower = self.getCurrentPower()
        
        totalpower = currentPower / 1000 / 3600 / 1000 * deltaTime
        #self.log(str(currentPower) + " W / " + str(totalpower) + "kW/h")
        self.addEnergyCounter( totalpower)

    def resetEnergyCounter(self):
        self.states["resetEnergyCounter"] = False
        self.states["energyCounter"] = 0.0

    def setState(self, name, value):    
        super().setState(name, value)

        match name:
            case "on":
                # self.setPosition(value)
                self.turnOn(value)
                pass
            case "resetEnergyCounter":
                # self.setUp(value)
                self.resetEnergyCounter()
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