from SHDevices.sh_device import *

class SH_Sprinkler(SHDevice):

    def __init__(self,name, connection=None, device=None, states={}, fields={}):
        super().__init__(name, connection, device, states, fields)        

        # add Devices
        # self.motor_position = device.getDevice("position sensor")
        # self.motor_position.enable(device.getBasicTimeStep())

        # add states
        super().add_state(name='hideSprinkler',value=True, description="Retract Sprinkler", min=None, max=None, unit=None)
        super().add_state(name='waterFlow',value=0, description="Retract Sprinkler", min=0, max=1, unit='%')

        # add fields
        super().add_field('sprinklerFlow', self.device.getSelf().getField("sprinklerFlow"))
        super().add_field('hideSprinkler', self.device.getSelf().getField("hideSprinkler"))
        super().add_field('waterTransparency', self.device.getSelf().getField("waterTransparency"))
        super().add_field('waterHeight', self.device.getSelf().getField("waterHeight"))
        super().add_field('waterRadius', self.device.getSelf().getField("waterRadius"))
        super().add_field('sprinklerPos', self.device.getSelf().getField("sprinklerPos"))
        super().add_field('waterScale', self.device.getSelf().getField("waterScale"))


        
        self.upPosition = 0.035
        self.downPosition = 0.0
        self.waterTransparency = 0.7

        self.maxWaterHeight = self.getWaterHeight()
        self.maxWaterRadius = self.getWaterRadius()
    
    # get Transform from Device
    def getTransform(self):
        return self.device.getSelf().getField("translation").getSFVec3f()

    def setWaterTransparency(self, value):
        self.waterTransparency = self.getWaterTransparency()
        self.fields['waterTranspareny'].setSFFloat(value)

    def getWaterTransparency(self, value):
        return self.fields['waterTranspareny'].getSFFloat()


    def getSprinklerPosition(self):
        return self.fields["sprinklerPos"].getSFVec3f()

    def setSprinklerPos(self, value):
        self.fields["sprinklerPos"].setSFVec3f([0,0,value])

    def getWaterHeight(self):
        return self.fields["waterHeight"].getSFFloat()

    def setWaterHeight(self, value):
        self.fields["waterHeight"].setSFFloat(value)

    def getWaterRadius(self):
        return self.fields["waterRadius"].getSFFloat()
    
    def setWaterRadius(self, value):
        self.fields["waterRadius"].setSFFloat(value)

    def setWaterScale(self, x,y,z):
        self.fields["waterScale"].setSFVec3f([x,y,z])

    def hideSprinkler(self, value):
        self.log('HIDE ' + str(value))
        if value:
            self.setSprinklerPos(self.downPosition)
        else:
            self.setSprinklerPos(self.upPosition)
        

    def setWaterFlow(self, value):
        self.log('FLOW ' + str(value))
        self.log(self.fields["sprinklerFlow"].getSFFloat())
        self.fields["sprinklerFlow"].setSFFloat(value)

        self.setWaterScale( self.getWaterRadius() * value, self.getWaterRadius() * value, self.getWaterHeight() * value )



    # message received
    def setState(self, name, value):    

        match name:
            case "hideSprinkler":
                self.hideSprinkler(value)
                pass
            case "waterFlow":
                if value == 0:
                    value = 0.001
                    #self.setWaterTransparency(1.0)
                
                self.setWaterFlow(value)
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