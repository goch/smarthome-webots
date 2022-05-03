"""SH Controller Template controller."""

from controller import Robot
from controller import Supervisor

from SHDevices.sh_device import *
# from SHDevices.sh_shutter import *

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
print(_CFG)




# create connection object
# create connection object
# ws = WebSocketClient(uri=_CFG["websocket"]["url"],open_cb=connected,
#                                                  close_cb=closed,
#                                                  message_cb=message_cb,
#                                                  error_cb=error)
# ws.start()

# create instance of SmartHome Device
# sh_device = SH_Shutter(robot.getName(), connection=ws, device=lamp)


# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    
    pass

# cleanup on Exit
