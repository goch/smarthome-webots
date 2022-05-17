"""ShutterController controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
from controller import Supervisor

import os
from config.definitions import ROOT_DIR, _CFG

from SHDevices.sh_shutter import *
from SHDevices.iobroker_websocket import *




def connected(ws):
    global shutter
    shutter.log("Connected")
    shutter.register()
    
def error(ws, error):
    global shutter
    shutter.log("Error -> " + str(error))

def closed(ws, close_status_code, close_msg):
    global shutter
    shutter.log("Disconected")
    pass

def web_message_cb(message):
    global shutter
    if message =="WINDOW_OPEN":
        shutter.emitt(True)
    elif message =="WINDOW_CLOSED":
        shutter.emitt(False)
    else:
        message_cb(None, message)


def message_cb(ws, message):
    global shutter
    shutter.log("new message -> " + str(message))
    shutter.setState(message["property"], message["value"])
    

TIME_STEP = 64
# create the Robot instance.
robot = Supervisor()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

deltaTime = 0

# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getDevice('motorname')
#  ds = robot.getDevice('dsname')
#  ds.enable(timestep)


# motor = robot.getDevice('linear motor')
# position = robot.getDevice("position sensor")
# motor.setPosition(1.3)
#position.enable(TIME_STEP)

ws = WebSocketClient(uri=_CFG["websocket"]["url"],open_cb=connected ,close_cb=closed,message_cb=message_cb, error_cb=error)
shutter = SH_Shutter(robot.getName(),connection=ws,device=robot)
shutter.connect()


lastPosition = 0

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    deltaTime += timestep
    shutter.receive_webui(web_message_cb)
        
    
    # TODO ALSO UPDATE CURRENT POSITION IF TARGET POSITION REACHED
    # do something every 1000ms
    if deltaTime > 1000: 
        shutter.updateCurrentPosition()
        deltaTime = 0

    pass

