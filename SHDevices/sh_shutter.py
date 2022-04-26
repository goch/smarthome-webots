from sh_device import SHDevice

class SH_Shutter(SHDevice):

    def __init__(self,name, device, emitter=None, receiver=None, states={}, fields={}):
        super().__init__(name, device, emitter, receiver, states, fields)        

        super().add_state('setPostion',1.3)
        super().add_state('up',False)
        super().add_state('down',False)
        super().add_state('stop',True)
        super().add_state('currentPosition',1.3)

        #super().add_field('position',device.getField("pointLightColor"))
        #super().add_field('velocity',device.getField("pointLightColor"))

        self.motor = self.device.getDevice("linear motor")
        self.motor.setPosition(1.3)
    
        self.reset()

    def set_state(self, name,value):
        super().set_state(name,value)

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
    
    def reset(self):
        # self.set_state('r',1)
        # self.set_state('g',1)
        # self.set_state('b',1)
        # self.set_state('brightness',1)
        # self.set_state('on',False)
        pass
            
