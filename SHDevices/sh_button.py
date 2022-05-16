from random import setstate
from SHDevices.sh_device import *

class SH_Button(SHDevice):

    def __init__(self,name, connection=None, device=None, buttonCount=2, states={}, fields={}):
        super().__init__(name, connection, device, states, fields)        
                

        for x in range(1,buttonCount+1):
            #self.log("addState: button "+ str(x))
            super().add_state('button'+ str(x) +'_pressed_short',False)
            super().add_state('button'+ str(x) +'_pressed_long',False)
            super().add_state('button'+ str(x) +'_pressed_double',False)


        # self.reset()    

    def setState(self, name, value):    

        if name in self.states:
            self.setStateValue(name, value)
        else: 
            self.log("State:" + name + " not in states")
    
    def register(self):
        super().register()


    def reset(self):
        super().reset()
        # self.set_state('setPosition',1.3)
        self.sendReset()
        pass