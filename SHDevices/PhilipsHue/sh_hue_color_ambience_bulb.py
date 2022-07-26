from SHDevices.sh_device import *
from SHDevices.sh_rgblight import SH_RGBLight

class SH_hue_color_ambience_bulb(SH_RGBLight):

    def __init__(self,name, connection=None, device=None, states={}, fields={}):
        super().__init__(name, connection, device, states, fields)        

        # add Devices
        # self.motor_position = device.getDevice("position sensor")
        # self.motor_position.enable(device.getBasicTimeStep())
        # add states
        super().add_state(name='brightness',value=100, description="Brightness in percent", min=0, max=100, unit='%')
        super().add_state(name='brightness_move',value=0, description="brightness change per second")
        super().add_state(name='color',value='#FFFFFF', description="Color as HEX")
        super().add_state(name='colortemp',value=4500, description="Temperature in Kelvin", min=1, max=6500, unit='K')
        super().add_state(name='colortemp_startup',value=4500, description="Color Temp at turn on", min=0, max=6500)
        super().add_state(name='colortemp_move',value=0, description="Temperature change per second")
        super().add_state(name='effect',value="blink", description="Blinking")
        super().add_state(name='hue',value=100, description="Not Implemented", min=0, max=360)
        super().add_state(name='hue_calubration',value=0, description="Not Implemented")
        super().add_state(name='hue_move',value=0, description="Not Implemented")
        super().add_state(name='saturation',value=100, description="Not Implemented", min=0, max=360)
        super().add_state(name='saturation_move',value=100, description="Not Implemented")
        super().add_state(name='transition_time',value=0, description="time in Seconds to transition to new value")
        super().add_state(name='state',value=True, description="Switch State")

        super().remapState('on','state')
        super().ignoreState('r')
        super().ignoreState('g')
        super().ignoreState('b')

        self.deltaTime = 0
        
        self.currentSaturation = 0
        self.currentBrightness = 0
        self.currentColorTemp = 0

        self.transitions = {}

        # add fields
        #super().add_field('position',device.getField("pointLightColor"))
    
    def getBrightnessMove(self):
        return self.getStateValue('brightness_move')

    def getBrightness(self):
        return self.getStateValue('brightness')
    
    def getColorTempMove(self):
        return self.getStateValue('colortemp_move')

    def getColorTemp(self):
        return self.getStateValue('colortemp')

    def setBrightnessMove(self,value):
        self.setStateValue('brightness_move',value)
           
    def setColorTempMove(self,value):
        self.setStateValue('colortemp_move',value)

    def update(self, step):
        super().update(step)
        self.deltaTime += step

        if self.deltaTime >= 1000:
            self.deltaTime = 0

            if self.getBrightnessMove() != 0:
                #TODO brightnessValue of Webots light is in range 0-5 and move is in range 0-100
                self.currentBrightness += self.getBrightnessMove() 
                self.setLightBrightness(self.currentBrightness)
        
            if self.getColorTempMove() !=0:
                self.currentColorTemp = self.kelvin_to_mirred(self.getColorTemp()) + self.getColorTempMove()
                self.setColorTemperature(self.currentColorTemp)
        
    # message received
    def setState(self, name, value):    

        match name:
            case "brightness_move":
                self.setBrightnessMove(value)
                if value != 0:
                    self.currentBrightness = self.getBrightness()
                else:
                    self.log("updateBrightness: " + str(self.currentBrightness))
                    self.setBrightness(self.currentBrightness)
                pass
            case "colortemp_move":
                self.setColorTempMove(value)
                if value == 0:
                    self.setColorTemperature(self.currentColorTemp)
            case "hue":
                # self.setStop(value)
                pass
            case "saturation":
                # self.setStop(value)
                pass      
            case "transition_time":
                pass
            case "effect":
                pass      
            case _:
                self.log("resolve Remap for state: " + name)
                super().setState(self.resolveRemap(name), value)
                pass
    
    def register(self):
        super().register()

    def reset(self):
        super().reset()
        self.sendReset()
        pass