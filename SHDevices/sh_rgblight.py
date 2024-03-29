from SHDevices.sh_device import *
import math

class SH_RGBLight(SHDevice):

    def __init__(self, name, connection=None, device=None, states={}, fields={}):
        super().__init__(name, connection, device, states, fields)        
        
        super().add_field('lcolor', self.device.getSelf().getField("color"))
        super().add_field('brightness', self.device.getSelf().getField("brightness"))
        super().add_field('maxBrightness', self.device.getSelf().getField("maxBrightness"))

        super().add_state('color' ,value='#FFFFFF', description="Color as HEXString")
        super().add_state('colortemp' ,value='2000', description="Colortemperature in Kelvin", min=1, max=7000, unit='K')
        super().add_state('r',value=1, description="Red Intensity", min=0.0, max=1.0)
        super().add_state('g',value=1, description="Green Intensity", min=0.0, max=1.0)
        super().add_state('b',value=1, description="Blue Intensity", min=0.0, max=1.0)
        super().add_state('brightness',value=5, description="Webots Brightness Value", min=0, max=self.fields['maxBrightness'].getSFFloat())
        super().add_state('on',value=False, description="ON/OFF")

        self.lastColor = self.getLightColor()
        self.meshColor = self.fields['lcolor'].getSFColor()
        self.setBrightness(self.getBrightness())
        #super().add_field('emission', self.device.getSelf().getField("emissiveIntensity"))

        
        self.lastBrightness = self.getLightBrightness()
        

    def kelvin_to_mirred(self,temperature):
        if temperature < 600:
            return temperature
        else:
            return int( 1e6 / temperature )

    def kelvin_to_rgb(self, kelvin, normalize=True):
        # convert from mirred scale to kelvin
        if kelvin <= 600:
            kelvin = 1000000 / kelvin

        # approximate rgb color from kelvin
        temperature = kelvin / 100
        if temperature <= 66: Red = 255
        else:
            Red = temperature - 60
            Red = 329.698727446 * math.pow(Red, -0.1332047592)
            if Red < 0: Red = 0
            if Red > 255: Red = 255

        if temperature <= 66:
            Green = temperature
            Green = 99.4708025861 * math.log(Green) - 161.1195681661
        else:
            Green = temperature - 60
            Green = 288.1221695283 * math.pow(Green,-0.0755148492)

        if Green < 0: Green = 0
        if Green > 255: Green = 255


        if temperature >= 66: Blue = 255
        else:
            if temperature <= 19: Blue = 0
            else:
                Blue = temperature - 10
                Blue = 138.5177312231 * math.log(Blue) - 305.0447927307
                if Blue < 0: Blue = 0
                if Blue > 255: Blue = 255

        if normalize:
            return self.normalizeRGB(Red,Green,Blue)
        else:
            return [Red,Green,Blue]


    def hex_to_rgb(self,hex, normalize=True):
        hex = hex.lstrip('#')
        rgb = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
        if normalize:
            return self.normalizeRGB(rgb[0],rgb[1],rgb[2])
        else:
            return rgb

    def hsv_to_rgb(self ,h, s, v,normalize=True):
            if normalize:
                h= h/360
                s= s/100
                v= v/100

            if s == 0.0: return [v, v, v]
            i = int(h*6.) # XXX assume int() truncates!
            f = (h*6.)-i; p,q,t = v*(1.-s), v*(1.-s*f), v*(1.-s*(1.-f)); i%=6
            if i == 0: return [v, t, p]
            if i == 1: return [q, v, p]
            if i == 2: return [p, v, t]
            if i == 3: return [p, q, v]
            if i == 4: return [t, p, v]
            if i == 5: return [v, p, q]

    def rgb_to_hsv(self, r, g, b):
        mx = max(r, g, b)
        mn = min(r, g, b)
        df = mx-mn
        if mx == mn:
            h = 0
        elif mx == r:
            h = (60 * ((g-b)/df) + 360) % 360
        elif mx == g:
            h = (60 * ((b-r)/df) + 120) % 360
        elif mx == b:
            h = (60 * ((r-g)/df) + 240) % 360
        if mx == 0:
            s = 0
        else:
            s = (df/mx)*100
        v = mx*100
        return [h, s, v]

    def normalizeRGB(self,r,g,b):
        return r/255, g/255, b/255

    def getRGBColor(self):
        return self.getStateValue('r'), self.getStateValue('g'), self.getStateValue('b')

    def getHexColor(self):
        return self.getStateValue('color')

    def getLightColor(self):
        return self.fields['lcolor'].getSFColor()

    def setLightColor(self,rgb):
        self.fields['lcolor'].setSFColor(list(rgb))
        self.lastColor = rgb
        self.log(self.lastColor)

    def setLightTemperature(self,kelvin):
        self.setLightColor(self.kelvin_to_rgb(kelvin))

    def setColorTemperature(self,value):
        self.setStateValue('colortemp',value)
        self.setLightColor(self.kelvin_to_rgb(value))


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

        self.setLightColor([r,g,b])

    def setLightBrightness(self,value):
        if value <0: value = 0
        self.fields['brightness'].setSFFloat(value * ( self.fields['maxBrightness'].getSFFloat() / self.getState('brightness').getMax()))

    def getLightBrightness(self):
        return self.fields['brightness'].getSFFloat()

    def turnOn(self, on):
        if on:
            self.setStateValue('on', True)
            self.setLightBrightness(self.getBrightness())
            self.setLightColor(self.lastColor)
        else:
            #TODO FIX Lamp Emitting light even if it is off
            self.setStateValue('on', False)
            self.setLightBrightness(0)
            self.lastColor = self.getLightColor()

        #self.updateMeshColor()

    def getBrightness(self):
        return self.getStateValue('brightness')

    def setBrightness(self,value):
        self.setStateValue('brightness', value)
        self.setLightBrightness(value)
        if value > 0:
            self.turnOn(True)
        else:
            self.turnOn(False)

    def updateMeshColor(self):
        #TODO change color of bulb based on brightness
        self.setColor(hex=self.getHexColor())
        pass

    def update(self, step):
        pass

    def setState(self, name,value):
        match name:
            case "color":
                self.setColor(hex=value)
            case "colortemp":
                self.setColorTemperature(value)
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
                    self.setLightBrightness(self.getBrightness())
                else:
                    self.setLightBrightness(0)
            case "brightness":
                self.setBrightness(value)

            case _:
                print("state not found")
    
    def register(self):
        super().register()
    
    def reset(self):
        super().reset()
        self.sendReset()


