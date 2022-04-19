import json
class SHDevice(object):

    def __init__(self, name, device, states={}, fields={}):
        self.device = device  
        self.name = name
        self.states = states
        self.fields = fields

    def add_state(self, name, value):
        self.states[name] = value

    def add_field(self, name,value):
        self.fields[name] = value

    def set_state(self, name,value):
        print("setState "+name+": " +str(value))
    
    def reset(self):
        print ("reset:"+name) 

    # def set_SFColor(value):
    #     for n in range(len(value)):
    #         if value[n] != 0:
    #             value[n] = 1.0/value[n]]

    def toJSON(self):
        return json.dumps({"name": self.name, "data": self.states})
    

    def __str__(self):
        string = ""
        for key, value in self.states.items():
            string += key + ": " + str(value) +"\n"

        string += "\n"
        for key, value in self.fields.items() :
            string += key + ": " + str(value) +"\n"
        
        return string



    
class WB_FloorLight(SHDevice):

    def __init__(self,name, device,states={}, fields={}):
        super().__init__(name,states,fields)
        
        super().add_state('r',0)
        super().add_state('g',0)
        super().add_state('b',0)
        super().add_state('brightness',0)
        super().add_state('on',False)

        super().add_field('lcolor',device.getField("pointLightColor"))
        super().add_field('bcolor',device.getField("bulbColor"))
        super().add_field('brightness',device.getField("pointLightIntensity"))
    
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
        self.set_state('r',1)
        self.set_state('g',1)
        self.set_state('b',1)
        self.set_state('brightness',1)
        self.set_state('on',False)
            
