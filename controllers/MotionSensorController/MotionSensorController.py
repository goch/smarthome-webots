"""SH Controller Template controller."""

from controller import Robot
from controller import Supervisor

from SHDevices.sh_device import *
from SHDevices.sh_motion_sensor import *

import json
from config.definitions import ROOT_DIR, _CFG

def connected(ws):
    global sh_device
    sh_device.log("Connected")
    sh_device.register()

    
def error(ws, error):
    global sh_device
    sh_device.log("Connection Error -> " + str(error))

def closed(ws, close_status_code, close_msg):
    global sh_device
    sh_device.log("Disconected")
    pass

def web_message_cb(message):
    global sh_device
    if message == "---- WINDOW LOADED ----":
        sh_device.register()
    else:
        message_cb(None, message)

def message_cb(ws, message):
    global sh_device
    sh_device.log("new message -> " + message)
    try:
        msg = json.loads(message)
        sh_device.setState(msg["property"], msg["value"])
    except Exception as e:
        sh_device.log(str("Message Error: " + str(e)))
        return

TIME_STEP = 64
robot = Supervisor()
timestep = int(robot.getBasicTimeStep())




# create connection object
ws = WebSocketClient(uri=_CFG["websocket"]["url"],open_cb=connected,
                                                 close_cb=closed,
                                                 message_cb=message_cb,
                                                 error_cb=error)

# create instance of SmartHome Device
sh_device = SH_Motion_Sensor(robot.getName(), connection=ws, device=robot)
sh_device.connect()

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    
    sh_device.getMotionDetected()
    # check if messages are send from WebUI 
    sh_device.receive_webui(web_message_cb)
    
    pass

# cleanup on Exit
