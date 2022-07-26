"""SH Controller Template controller."""

from controller import Robot
from controller import Supervisor

from config.definitions import CONFIG
from SHConnection.sh_connection import CONECTION

from SHDevices.sh_smokedetector import *
from math import sqrt, pow


def getDistance(x1,y1,x2,y2):
    return sqrt( pow((x1 - x2),2) + pow((y1 - y2),2))

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
connection_config = CONFIG.getDeviceConnection(robot.getName())
connection  = CONECTION.create(key=connection_config['type'], **connection_config) 
connection.register_callbacks(connected, closed, error, message_cb)

# create instance of SmartHome Device
sh_device = SH_SmokeDetector(robot.getName(), connection=connection, device=robot)
sh_device.connect()

deltaTime = 0

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:

    deltaTime += timestep
    
    # measure data every 10s
    if deltaTime > 10000:
        deltaTime = 0
        
        if sh_device.checkFire():
            sh_device.triggerAlarm()
        #fires = sh_device.device.getFromDef("FIRE")
        # human_name = humans.getField("name").getSFString()

        if sh_device.getTest():
            sh_device.runTest(timestep)

        sh_device.drainBattery(timestep)

    # check if messages are send from WebUI 
    sh_device.receive_webui(web_message_cb)
    pass

# cleanup on Exit
sh_device.log("---- CLEANUP ----")
sh_device.disconnect()