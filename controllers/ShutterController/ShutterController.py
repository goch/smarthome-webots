"""ShutterController controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
from controller import Supervisor

import os
from config.definitions import ROOT_DIR, _CFG
from SHDevices.sh_device import *
from SHDevices.sh_shutter import *
import json


def log(msg):
    global robot
    print(robot.getName() + ":" + msg)

def connected(ws):
    global shutter
    log("Connected")
    shutter.register()
    #msg = device.toJSON()
    
def error(ws, error):
    global shutter
    shutter.log("Connection Error -> " + str(error))

def closed(ws, close_status_code, close_msg):
    global shutter
    log("Disconected")
    pass

def web_message_cb(message):
    global shutter
    if message == "---- WINDOW LOADED ----":
        shutter.register()
    else:
        message_cb(None, message)


def message_cb(ws, message):
    global shutter
    log("new message -> " + message)
    try:
        msg = json.loads(message)
        shutter.setState(msg["property"], msg["value"])
    except Exception as e:
        log(str("Message Error: " + str(e)))
        return

TIME_STEP = 64
# create the Robot instance.
robot = Supervisor()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())


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
delta = (shutter.motor.getMaxPosition() - shutter.motor.getMinPosition()) / 25

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:

    shutter.receive_webui(web_message_cb)
        
    currentPosition = shutter.motor_position.getValue()
    currentDelta = abs(lastPosition - currentPosition)
    
    if currentDelta >= delta:
        lastPosition = currentPosition
        shutter.updateCurrentPosition(currentPosition)


    pass

