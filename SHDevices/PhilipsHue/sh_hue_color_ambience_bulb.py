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
        super().add_state(name='colortemp',value=150, description="Temperature in Kelvin", min=1, max=7000, unit='K')
        super().add_state(name='colortemp_startup',value=4500, description="Color Temp at turn on", min=1, max=7000)
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
        self.lastColorTemp = self.getColorTemp()
        self.colorTempMove = False
        self.BrightnessMove = False
        self.lastBrightness = self.getBrightness()

        self.lastHSV = (0,0,0)
        self.hueMove = False
        self.transition_steps = 0
        self.command = []
        self.commandList =[]
        self.commandExpanded = False
        

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
           
    def getHueMove(self):
        return self.getStateValue("hue_move")

    def setColorTempMove(self,value):
        self.setStateValue('colortemp_move',value)

    def getTransitionTime(self):
        return self.getStateValue('transition_time')

    def setCommand(self, name,value):
        self.command = [name,value]
        self.commandList = []
        self.commandExpanded = False
    
    def getCommandName(self):
        return self.command[0]

    def getCommandValue(self):
        return self.command[1]

    def expandCommand(self,step):
        transition_steps = self.getTransitionTime() / self.getCommandValue() 
        transition_value = (self.getCommandValue() - self.getStateValue(self.getCommandName())) / transition_steps
        
        value = self.getStateValue(self.getCommandName())
        while transition_steps >= 0:
            self.commandList.append(value + transition_value )
            transition_steps -= 1
        self.commandExpanded = True

    def enableHueMove(self, enable,value=0):
        if enable:
            self.hueMove = True
            self.lastHSV = value
        else:
            self.hueMove = False
            #self.setStateValue('Hue',self.lastHSV[0])

    def enableBrightnessMove(self,enable):
        if enable:
            self.BrightnessMove = True
            self.lastBrightness = self.getBrightness()
        else:
            self.BrightnessMove = False
            self.setBrightness(self.lastBrightness)

    def enableColorTempMove(self, enable):
        if enable:
            self.colorTempMove= True
            self.lastColorTemp = self.kelvin_to_mirred(self.getColorTemp())
        else:
            self.colorTempMove = False
            self.setColorTemperature(self.lastColorTemp)
        


    def update(self, step):
        super().update(step)
        self.deltaTime += step

        # #check if command expanded
        # if self.command and self.commandExpanded is False:
        #     self.expandCommand(step)

        
        # if len(self.commandList) != 0:
        #     self.setStateValue(self.getCommandName(),self.commandList.pop(0))

        if self.hueMove:
            move = self.getHueMove()
            self.lastHSV[0] += move / 33
            rgb = self.hsv_to_rgb(self.lastHSV[0],self.lastHSV[1],self.lastHSV[2])            
            self.setLightColor(rgb)

       
        if self.BrightnessMove:
            move = self.getBrightnessMove()
            self.lastBrightness += move / 90
            if self.lastBrightness < 5: 
                self.lastBrightness = 5
                self.enableBrightnessMove(False)
            if self.lastBrightness > 100:
                self.lastBrightness = 100    
                self.enableBrightnessMove(False)
        
            self.setLightBrightness(self.lastBrightness)
    
        if self.colorTempMove:
            move = self.getColorTempMove()
            self.lastColorTemp += move / 64
            if self.lastColorTemp < 150: 
                self.lastColorTemp = 150
                self.enableColorTempMove(False)
            if self.lastColorTemp > 500:
                self.lastColorTemp = 500    
                self.enableColorTempMove(False)

            self.setLightTemperature(self.lastColorTemp)
    
    # message received
    def setState(self, name, value):    
        self.enableHueMove(False)
        self.enableBrightnessMove(False)
        self.enableColorTempMove(False)
        match name:
            case "brightness_move":
                self.setBrightnessMove(value)
                if value != 0:
                    self.enableBrightnessMove(True)
                pass
            case "colortemp":
                self.lastColorTemp = value
                super().setState(self.resolveRemap(name), value)
            case "colortemp_move":
                self.setColorTempMove(value)
                if value != 0:
                    self.enableColorTempMove(True)
            case "hue":
                self.setStateValue(name,value)
                pass
            case "hue_move":
                (r,g,b) = self.getLightColor()               
                hsv =self.rgb_to_hsv(r,g,b)
                (h,s,v) = hsv
                rgb = self.hsv_to_rgb(h,s,v)

                self.enableHueMove(True,hsv)
                self.setStateValue(name,value)
                
            case "saturation":
                self.setStateValue(name,value)
                pass      
            case "transition_time":
                self.setStateValue("transition_time",value)
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