from SHDevices.sh_device import *

class SH_PowerPlug(SHDevice):

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
        self.setStateValue('on',state)
        if state:
            self.setCurrentPower(9000)
        else:
            self.setCurrentPower(0)
        pass

    def setLED(self,state):
        self.led.set(int(state))

    def setCurrentPower(self,value):
        self.setStateValue('currentPowerConsumption',value)
    
    def getCurrentPower(self):
        return self.getStateValue('currentPowerConsumption')

    def addEnergyCounter(self,value):
        if value == 0:
            return

        self.setStateValue('energyCounter', self.getStateValue('energyCounter') + value) 

    def updateEnergyCounter(self, deltaTime):
        currentPower = self.getCurrentPower()
        
        totalpower = currentPower / 1000 / 3600 / 1000 * deltaTime
        #self.log(str(currentPower) + " W / " + str(totalpower) + "kW/h")
        self.addEnergyCounter( totalpower)

    def resetEnergyCounter(self):
        self.setStateValue('resetEnergyCounter', False)
        self.setStateValue('energyCounter', 0.0)

    def setState(self, name, value):    

        match name:
            case "on":
                self.turnOn(value)
                pass
            case "resetEnergyCounter":
                self.resetEnergyCounter()
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