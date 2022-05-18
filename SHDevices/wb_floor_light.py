from SHDevices.sh_device import *

class WB_FloorLight(SHDevice):

    def __init__(self, name, connection=None, device=None, states={}, fields={}):
        super().__init__(name, connection, device, states, fields)        
        
        self.lamp = device.getSelf().getField("children").getMFNode(0)

        super().add_state('r',1)
        super().add_state('g',1)
        super().add_state('b',1)
        super().add_state('brightness',1)
        super().add_state('on',False)

        super().add_field('lcolor', self.lamp.getField("pointLightColor"))
        super().add_field('bcolor', self.lamp.getField("bulbColor"))
        super().add_field('brightness', self.lamp.getField("pointLightIntensity"))
    
        # self.reset()

    def setState(self, name,value):

        match name:
            case "r":
                self.setStateValue('r', value)
                if self.states["on"]:
                    self.fields['lcolor'].setSFColor([value,self.getStateValue('g'),self.getStateValue('b')])
                    self.fields['bcolor'].setSFColor([value,self.getStateValue('g'),self.getStateValue('b')])
            case "g":
                self.setStateValue('g', value)
                if self.getStateValue('on'):
                    self.fields['lcolor'].setSFColor([self.getStateValue('r'),value,self.getStateValue('b')])
                    self.fields['bcolor'].setSFColor([self.getStateValue('r'),value,self.getStateValue('b')])
            case "b":
                self.setStateValue('b', value)
                if self.getStateValue('on'):
                    self.fields['lcolor'].setSFColor([self.getStateValue('r'),self.getStateValue('g'),value])
                    self.fields['bcolor'].setSFColor([self.getStateValue('r'),self.getStateValue('g'),value])
            case "on":
                self.setStateValue('on', value)
                if self.getStateValue('on'):
                    self.fields['brightness'].setSFFloat(self.getStateValue('brightness'))
                    self.fields['lcolor'].setSFColor([self.getStateValue('r'),self.getStateValue('g'),self.getStateValue('b')])
                    self.fields['bcolor'].setSFColor([self.getStateValue('r'),self.getStateValue('g'),self.getStateValue('b')])
                else:
                    self.fields['brightness'].setSFFloat(0)
                    self.fields['bcolor'].setSFColor([1,1,1])
            case "brightness":
                self.setStateValue('brightness', value) 
                self.fields['brightness'].setSFFloat(value)
                if value >0:
                    self.setStateValue('on', True)

                else:
                    self.setStateValue('on', False)
                    self.fields['bcolor'].setSFColor([1,1,1])

            case _:
                print("state not found")
    
    def register(self):
        super().register()
    
    def reset(self):
        super().reset()
        # self.getStateValue('r') =1
        # self.states['g'] =1    
        # self.getStateValue('b') =1
        # self.states['brightness'] =1
        # self.states['on'] = False
        self.sendReset()


