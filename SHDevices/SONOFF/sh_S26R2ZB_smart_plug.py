from SHDevices.sh_powerplug import *

class SH_S26R2ZB_smart_plug(SH_PowerPlug):

    def __init__(self,name, connection=None, device=None, states={}, fields={}):
        super().__init__(name, connection, device, states, fields)        

        super().add_state('battery', description='Battery percent', value=98, unit='%')
        super().add_state('voltage', description='Battery voltage',value=3.3, unit='V')
        super().add_state('power_on_behavior', description='Controlls the behavior if the device is powered on',value="Off" )
        super().add_state('state', description='On/Off state of the switch',value=False )


        # add fields
        #super().add_field('position', self.device.getSelf().getField("pointLightColor"))

        # remap states
        super().remapState('on','state')
        super().ignoreState('currentPowerConsumption')
        super().ignoreState('energyCounter')
        super().ignoreState('resetEnergyCounter')
    
    # get Transform from Device
    def getTransform(self):
        return self.device.getSelf().getField("translation").getSFVec3f()
    
    def update(self, step):
        self.deltaTime +=step
        super().update(step)
        pass

    # message received
    def setState(self, name, value):    

        match name:
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