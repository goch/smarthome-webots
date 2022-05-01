"""smart_home_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import supervisor, Motor, DistanceSensor
from controller import Supervisor, Robot
import struct
import json
from sh_device import *
from wb_floor_light import *
#websocket Server
import threading
import logging
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

class Device(object):
    def __init__(self, name, channel):
        self.name = name
        self.channel = channel




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
            # print(type(supervisor))
            # rgbLight = supervisor.getFromDef("RGBLight")
            # print(type(rgbLight))
            # if msg.get("property") == 'brightness':
                    # rgbLight.getField("pointLightIntensity").setSFFloat(value)
                    
            # device = DDB.get(msg.name)
            # print(device.name)
            # device.set_state(msg.property,msg.value)
            
            # dev = DDB.get("RGBLamp")
            # dev.set_state(msg.get("property"),msg.get("value"))
            #print (dev)
            pass
                
         


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
    

def getNode(scope):
    nodes = scope.split(".")
    print(nodes)
    device = None
    for node in nodes:
        print("Looking for Node:" + node)
        if device != None:
            device = device.getField(node)
        else:
            device = supervisor.getFromDef(node)
            
    

    return device



#wss = WebSocketThread()
#wss.start()

# create the supervisor instance.
global supervisor
supervisor = Supervisor()
#robot = Robot()

emitter = supervisor.getDevice("emitter")  
receiver = supervisor.getDevice("receiver")  
receiver.enable(33)


global DDB

DDB ={}

dev = supervisor.getFromDef("RGBLight")
rgbLamp = WB_FloorLight(name="RGBLamp",device=dev)
DDB[rgbLamp.name] = rgbLamp


# print("---- SHUTTER ----")
# shutter= supervisor.getFromDef("SH_SHUTTER")
# motor = supervisor.getFromDef("SH_SHUTTER.WINDOW.GLASS.JOINT.MOTOR")
# #motor = getNode("SH_SHUTTER.children.window.children.glass.children.sliderJoint")

# linearm = supervisor.getFromDevice(motor)

# print (type(shutter), shutter)
# print (type(motor), motor.getTypeName())

#print (linearm.getName(), type(linearm), linearm.getTypeName())
#motor = motor.getDevice("")
#motor.setPosition(1.3)


print("DDB:")
for name, device in DDB.items():
    print("-- "+name+"--") 
    print (device)
    # print(device.toJSON())
    # data = json.loads(device.toJSON())
    # print (data["name"])
    # print (data["data"])


# dev = DDB.get("RGBLamp")
# dev.set_state("brightness",1.0)

# print (dev)


# get the time step of the current world.
timestep = int(supervisor.getBasicTimeStep())

# You should insert a getDevice-like function in order to get the
# instance of a device of the supervisor. Something like:
#  motor = supervisor.getDevice('motorname')
#  ds = supervisor.getDevice('dsname')
#  ds.enable(timestep)




# Main loop:
# - perform simulation steps until Webots is stopping the controller
while supervisor.step(timestep) != -1:
    while receiver.getQueueLength() > 0:
        msg = receiver.getData()
        print("-- DATA PACKET RECEIVED! --")
        print(msg)
        
        try:
            data = json.loads(msg)
            print(data["type"])
            print("Send ACK to " + data["name"])
            ack = "OK!"
            #emitter.send(ack.encode("utf-8"))
            

        except Exception as e:
            print("Error parsing json: " + str(e))

        receiver.nextPacket()

    pass

# Enter here exit cleanup code.