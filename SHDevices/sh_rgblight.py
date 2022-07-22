from SHDevices.sh_device import *

class SH_RGBLight(SHDevice):

    def __init__(self, name, connection=None, device=None, states={}, fields={}):
        super().__init__(name, connection, device, states, fields)        
        
        super().add_state('color' ,value='#FFFFFF', description="Color as HEXString")
        super().add_state('r',1)
        super().add_state('g',1)
        super().add_state('b',1)
        super().add_state('brightness',value=5)
        super().add_state('on',False)

        super().add_field('lcolor', self.device.getSelf().getField("color"))
        super().add_field('brightness', self.device.getSelf().getField("brightness"))

        self.meshColor = self.fields['lcolor'].getSFColor()
        self.setBrightness(self.fields['brightness'].getSFFloat())
        self.setStateValue('brightness', self.fields['brightness'].getSFFloat())
        #super().add_field('emission', self.device.getSelf().getField("emissiveIntensity"))

        # self.reset()

    def hex_to_rgb(self,hex, normalize=True):
        hex = hex.lstrip('#')
        rgb = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
        if normalize:
            return self.normalizeRGB(rgb[0],rgb[1],rgb[2])
        else:
            return rgb

    def normalizeRGB(self,r,g,b):
        return r/255, g/255, b/255

    def getRGBColor(self):
        return self.getStateValue('r'), self.getStateValue('g'), self.getStateValue('b')

    def getHexColor(self):
        return self.getStateValue('color')

    def setColor(self,hex=None, r=None, g=None, b=None, send=True):
        if hex is not None:
            # convert to HEX
            (r,g,b) = self.hex_to_rgb(hex)
            if send:
                self.setStateValue('color',hex)
                self.setStateValue('r',r)
                self.setStateValue('g',g)
                self.setStateValue('b',b)
        else:
            if r == None:
                r = self.getStateValue('r')
            if g == None:
                g = self.getStateValue('g')
            if b == None:
                b = self.getStateValue('b')

        self.fields['lcolor'].setSFColor([r,g,b])

    def setBrightness(self,value):
        self.fields['brightness'].setSFFloat(value)
        if value > 0:
            self.setStateValue('on', True)
            self.updateMeshColor()
        else:
            self.setStateValue('on', False)
            #TODO FIX Lamp Emitting light even if it is off
            self.updateMeshColor()
            #self.setColor(r=self.meshColor[0],g=self.meshColor[1],b=self.meshColor[2])

    def updateMeshColor(self):
        #TODO change color of bulb based on brightness
        self.setColor(hex=self.getHexColor())
        pass

    def setState(self, name,value):
        match name:
            case "color":
                self.setColor(hex=value)
            case "r":
                self.setStateValue('r', value)
                if self.states["on"]:
                    self.setColor(r=value)
            case "g":
                self.setStateValue('g', value)
                if self.getStateValue('on'):
                    self.setColor(g=value)
            case "b":
                self.setStateValue('b', value)
                if self.getStateValue('on'):
                    self.setColor(b=value)
            case "on":
                self.setStateValue('on', value)
                if self.getStateValue('on'):
                    self.setBrightness(self.getStateValue('brightness'))
                else:
                    self.setBrightness(0)
            case "brightness":
                self.setStateValue('brightness', value) 
                self.setBrightness(value)

            case _:
                print("state not found")
    
    def register(self):
        super().register()
    
    def reset(self):
        super().reset()
        self.sendReset()


