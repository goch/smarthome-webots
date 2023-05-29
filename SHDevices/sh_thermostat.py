from SHDevices.sh_device import *

class SH_Thermostat(SHDevice):

    def __init__(self,name, connection=None, device=None, states={}, fields={}):
        super().__init__(name, connection, device, states, fields)        

        self.deltaTime = 0
        # add states
        super().add_state('setTemperature', description='Change Temperature',value=21, unit='°C')
        super().add_state('currentTemperature', description='Temperature',value=19, unit='°C')
        super().add_state('currentHumidity', description='Humidty',value=40, unit='%')
        super().add_state('setHumidity', description='Change Humidty',value=50, unit='%')
        # add fields
        #super().add_field('position',device.getField("pointLightColor"))
        # self.reset()    

    
    def setTemperature(self,value):
        self.setStateValue('setTemperature', value)

    def getSetTemperature(self):
        return self.getStateValue('setTemperature')
    
    def getCurrentTemperature(self):
        return self.getStateValue('currentTemperature')

    def updateCurrentTemperature(self,temperature):
        self.log("Update Temperature: " + str(temperature) + "/" + str(self.getSetTemperature()))
        self.setStateValue('currentTemperature', temperature)
        pass


    def setHumidity(self,value):
        self.setStateValue('setHumidity', value)

    def getSetHumidity(self):
        return self.getStateValue('setHumidity')
    
    def getCurrentHumidity(self):
        return self.getStateValue('currentHumidity')

    def updateCurrentHumidity(self,humidity):
        self.log("Update Humidity: " + str(humidity) + "/" + str(self.getSetTemperature()))
        self.setStateValue('currentHumidity', humidity)
        pass



    def update(self, step):
        self.deltaTime +=step
        # TODO: make heating system configurable
        # change temperature every 10s
        if self.deltaTime > 1000:
            self.deltaTime = 0
            currentTemp = self.getCurrentTemperature()
            setTemp = self.getSetTemperature()
            setHumidity = self.getSetHumidity()
            currentHumidity = self.getCurrentHumidity()

            if currentTemp < setTemp:
                # TODO heatup configurable
                # TODO PID controller to controll heatup decision
                self.updateCurrentTemperature(round(currentTemp + 0.1, 2))
            elif currentTemp > setTemp:
                self.updateCurrentTemperature(round(currentTemp - 0.1, 2))
                pass

            if currentHumidity < setHumidity:
                # TODO heatup configurable
                # TODO PID controller to controll heatup decision
                self.updateCurrentHumidity(round(currentHumidity + 0.1, 2))
            elif currentHumidity > setHumidity:
                self.updateCurrentHumidity(round(currentHumidity - 0.1, 2))
                pass

        pass

    def setState(self, name, value):    

        match name:
            case "setTemperature":
                self.setTemperature(value)
                pass
            case "setHumidity":
                self.setHumidity(value)
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