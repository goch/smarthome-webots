"""smart_home_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
from controller import Supervisor
import json
from sh_device import *
#websocket Server
import threading
import logging
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

class WebsocketServer(WebSocket):

    def handleMessage(self):
#        print(self.data)
        global DDB
        msg = json.loads(self.data)
        print(type(msg))
        print(msg)
        if type(msg) is str:
            match msg:
                case "Hello Webots":
                    print("RESET-SH")
                    self.sendMessage("RESET-SH")
#                case "SH-READY":
                    print("SENDING DEVICES:")
                    for name, device in DDB.items():
                        print("-- "+name+"--") 
                        print (device)
                        self.sendMessage(device.toJSON())
            
        else:
            # printMsg(msg)
            # value = msg.get("value")
            # name = msg.get("property")
            # setRGBProperty(name,value)
            # print(type(robot))
            # rgbLight = robot.getFromDef("RGBLight")
            # print(type(rgbLight))
            # if msg.get("property") == 'brightness':
                    # rgbLight.getField("pointLightIntensity").setSFFloat(value)
                    
            # device = DDB.get(msg.name)
            # print(device.name)
            # device.set_state(msg.property,msg.value)
            
            dev = DDB.get("RGBLamp")
            dev.set_state(msg.get("property"),msg.get("value"))
            #print (dev)
                
         


        # echo message back to client
        #self.sendMessage(self.data)
        
    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')


class WebSocketThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.port = 3000
        self.wsd = SimpleWebSocketServer('', self.port, WebsocketServer)
        self._logger = logging.getLogger(__name__)

    def getSocket(self):
        return self.wsd
        
    def run(self):
        #try:
            print("Websocket Server started on port %s" % self.port)
            self.wsd.serveforever()
        #except:
            print("WebSocket Crash!")



def printMsg(msg):
    print("State Message")
    print(msg.get("property"))
    print(msg.get("value"))
    print(type(msg.get("value")))
    

wss = WebSocketThread()
wss.start()

#socket = wss.getSocket()

#print("SendMessage")
#socket.sendMessage("Hello Webots")

# create the Robot instance.
global robot
robot = Supervisor()

#lamp = robot.getFromDef("lamp")
#lamplight = robot.getFromDef("lamplight")
#color = lamplight.getField("color")

#setRGB("RGBLight",[1,0,0] ,10)

#socket.sendMessage("Hello Webots")

#color.setSFColor([0,1,0])

# rgbdev = robot.getFromDef("RGBLight")
# brightness = rgbLight.getField("pointLightIntensity")
# brightness.setSFFloat(0)    


# bulb = rgbLight.getField("bulbColor")
# color = rgbLight.getField("pointLightColor")

# c = [0,1,0]

# bulb.setSFColor(c)
# color.setSFColor(c)

global DDB

DDB ={}

dev = robot.getFromDef("RGBLight")
rgbLamp = WB_FloorLight("RGBLamp",dev)
DDB[rgbLamp.name] = rgbLamp

print("DDB:")
for name, device in DDB.items():
    print("-- "+name+"--") 
    print (device)
    print(device.toJSON())
    data = json.loads(device.toJSON())
    print (data["name"])
    print (data["data"])


# dev = DDB.get("RGBLamp")
# dev.set_state("brightness",1.0)

# print (dev)


# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getDevice('motorname')
#  ds = robot.getDevice('dsname')
#  ds.enable(timestep)




# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:

    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()

    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    pass

# Enter here exit cleanup code.