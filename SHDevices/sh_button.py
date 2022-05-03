from SHDevices.sh_device import *

class SH_Button(SHDevice):

    def __init__(self,name, connection=None, device=None, buttonCount=2, states={}, fields={}):
        super().__init__(name, connection, states, fields)
                

        for x in range(1,buttonCount+1):
            self.log("addState: button "+ str(x))
            super().add_state('button'+ str(x) +'_pressed_short',False)
            super().add_state('button'+ str(x) +'_pressed_long',False)


        self.reset()    

    # 
    def setState(self, name, value):    
        super().setState(name, value)

        match name:
            case "setPosition":
                # self.setPosition(value)
                pass
            case "up":
                # self.setUp(value)
                pass
            case "down":
                # self.setDown(value)
                pass
            case "stop":
                # self.setStop(value)
                pass
            case _:
                print("state not found or state is read only")
                pass

        self.send(self.toJSON())
    
    def register(self):
        super().register()
        self.connection.send(self.toJSON())


    def reset(self):
        # self.set_state('setPosition',1.3)
        pass