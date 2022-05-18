"""Light Sensor controller."""

from controller import Robot
from controller import Supervisor

from SHDevices.sh_light_sensor import *
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


# create connection object
ws = WebSocketClient(uri=_CFG["websocket"]["url"],open_cb=connected,
                                                 close_cb=closed,
                                                 message_cb=message_cb,
                                                 error_cb=error) 

# create instance of SmartHome Device
sh_device = SH_Light_Sensor(robot.getName(), connection=ws,device=robot)
sh_device.connect()

last_luminosity = -1


# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    
    current_luminosity = sh_device.sensor.getValue()

    if current_luminosity != last_luminosity:
        last_luminosity = current_luminosity
        sh_device.updateLuminosity(current_luminosity)
         
    
    
    pass

# cleanup on Exit
sh_device.log("---- CLEANUP ----")
sh_device.disconnect()