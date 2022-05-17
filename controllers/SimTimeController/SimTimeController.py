"""SH Controller Template controller."""

from controller import Robot
from controller import Supervisor

from SHDevices.sh_sim_time import *
from SHDevices.iobroker_websocket import *

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
    message_cb(None, message)

def message_cb(ws, message):
    global sh_device
    sh_device.log("new message -> " + str(message))
    sh_device.setState(message["property"], message["value"])


TIME_STEP = 64
robot = Supervisor()
timestep = int(robot.getBasicTimeStep())
deltaTime = 0


# create connection object
ws = WebSocketClient(uri=_CFG["websocket"]["url"],open_cb=connected,
                                                 close_cb=closed,
                                                 message_cb=message_cb,
                                                 error_cb=error)

# create instance of SmartHome Device
sh_device = SH_Sim_Time(robot.getName(), connection=ws, device=robot,  hour=_CFG['simtime']['hour'], minute=_CFG['simtime']['minute'], second=_CFG['simtime']['second'] )
sh_device.connect()

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    deltaTime += timestep
    # check if messages are send from WebUI 
    sh_device.receive_webui(web_message_cb)

    # do something every 1000ms
    if deltaTime > 1000:
        sh_device.updateClock(deltaTime)
        deltaTime = 0
    pass

    pass

# cleanup on Exit
