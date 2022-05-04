from SHDevices.sh_device import *

class WB_FloorLight(SHDevice):

    def __init__(self, name, connection=None, device=None, states={}, fields={}):
        super().__init__(name, connection, device, states, fields)        
        
        super().add_state('r',0)
        super().add_state('g',0)
        super().add_state('b',0)
        super().add_state('brightness',0)
        super().add_state('on',False)

        super().add_field('lcolor', device.getField("pointLightColor"))
        super().add_field('bcolor', device.getField("bulbColor"))
        super().add_field('brightness', device.getField("pointLightIntensity"))
    
        self.reset()

    def setState(self, name,value):
        super().setState(name,value)

        match name:
            case "r":
                self.states['r'] = value
                if self.states["on"]:
                    self.fields['lcolor'].setSFColor([value,self.states['g'],self.states['b']])
                    self.fields['bcolor'].setSFColor([value,self.states['g'],self.states['b']])
            case "g":
                self.states['g'] = value
                if self.states["on"]:
                    self.fields['lcolor'].setSFColor([self.states['r'],value,self.states['b']])
                    self.fields['bcolor'].setSFColor([self.states['r'],value,self.states['b']])
            case "b":
                self.states['b'] = value
                if self.states["on"]:
                    self.fields['lcolor'].setSFColor([self.states['r'],self.states['g'],value])
                    self.fields['bcolor'].setSFColor([self.states['r'],self.states['g'],value])
            case "on":
                self.states['on'] = value
                if self.states['on']:
                    self.fields['brightness'].setSFFloat(self.states['brightness'])
                    self.fields['lcolor'].setSFColor([self.states['r'],self.states['g'],self.states['b']])
                    self.fields['bcolor'].setSFColor([self.states['r'],self.states['g'],self.states['b']])
                else:
                    self.fields['brightness'].setSFFloat(0)
                    self.fields['bcolor'].setSFColor([1,1,1])
            case "brightness":
                self.states['brightness'] = value 
                self.fields['brightness'].setSFFloat(value)
                if value >0:
                    self.states['on'] = True

                else:
                    self.states['on'] = False
                    self.fields['bcolor'].setSFColor([1,1,1])

            case _:
                print("state not found")

        self.send(self.toJSON())
    
    def register(self):
        super().register()
        self.connection.send(self.toJSON())

    
    def reset(self):
        self.states['r'] =1
        self.states['g'] =1    
        self.states['b'] =1
        self.states['brightness'] =1
        self.states['on'] = False