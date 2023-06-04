from SHDevices.sh_device import *


class SH_SNZB_04_door_window_sensor(SHDevice):

    def __init__(self,name, connection=None, device=None, states={}, fields={}):
        super().__init__(name, connection, device, states, fields)        

        # add Devices
        self.touch_sensor = device.getDevice("touch sensor")
        self.touch_sensor.enable(int(device.getBasicTimeStep()))

        # add states
        super().add_state('battery', description='Battery percent', value=98, unit='%')
        super().add_state('voltage', description='Battery voltage',value=3.3, unit='V')
        super().add_state('opened', description='Is open',value=False)
        super().add_state('contact', description='Contact Event',value=True)
        # add fields
        super().add_field('transform', self.getField("translation"))
        
        root_node = self.device.getRoot()
        tf = self.getTransform()
        rot = self.getRotation()
        #tf = tf + (rot *  (0.0, 0.02, 0.0))

        # BUG: if spawned close to the touch sensor, touch senser is not functioning correctly
        tf = str(tf[0]) + ' ' + str(tf[1]+0.08) + ' ' + str(1)

        self.log(str(rot))
        children_field = root_node.getField('children')
        children_field.importMFNodeFromString(-1,'Solid { name "SNZB-04_MAG" translation ' + tf + ' rotation 0 0 0 0 boundingObject Box {    size 0.032 0.015 0.013  } children [    Shape {      geometry Box {        size 0.032 0.015 0.013      }    }  ] }')
    
    # get Transform from Device
    def getTransform(self):
        return self.getFieldValue("translation")
    
    def getRotation(self):
        return self.getFieldValue("rotation")

    def update(self, step):
        self.deltaTime +=step
        if self.deltaTime == 1000:
            self.deltaTime = 0
            value = self.touch_sensor.getValue()
            self.log(value)
            self.setContact(bool(value))
        
        super().update(step)
        pass

    def setContact(self, value):
        self.setStateValue('contact',value)
        self.setStateValue('opened', not value)
    
    def setOpened(self, value):
        self.setStateValue('contact', not value)
        self.setStateValue('opened', value)

    # message received
    def setState(self, name, value):    

        match name:
            case "opened":
                self.setOpened(value)
            case "contact":
                self.setContact(value)
                pass
            case "voltage":
                pass
            case "battery":
                pass

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