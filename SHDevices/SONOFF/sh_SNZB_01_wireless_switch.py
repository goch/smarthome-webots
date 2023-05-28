from SHDevices.sh_device import *

class SH_SNZB_01_wireless_switch(SHDevice):

    def __init__(self,name, connection=None, device=None, states={}, fields={}):
        super().__init__(name, connection, device, states, fields)        

        super().add_state('battery', description='Battery percent', value=100, unit='%')
        super().add_state('click', description='Click event', value=False)
        super().add_state('long_click',description='Long click event', value=False)
        super().add_state('double_click',description='Double click event', value=False)
        super().add_state('voltage', description='Battery voltage',value=3.4, unit='V')


    
    # get Transform from Device
    def getTransform(self):
        return self.device.getSelf().getField("translation").getSFVec3f()
    
    def update(self, step):
        #self.deltaTime +=step
        pass    

    def setState(self, name, value):    
        match name:
            case "battery":
                self.setStateValue(name,value)
            case "click":
                self.setStateValue(name,value)
            case "long_click":
                self.setStateValue(name,value)
            case "double_click":
                self.setStateValue(name,value)
            case "voltage":
                self.setStateValue(name,value)
            case _:
                print("state not found")
    
    def register(self):
        super().register()

    def reset(self):
        super().reset()
        self.sendReset()
        pass