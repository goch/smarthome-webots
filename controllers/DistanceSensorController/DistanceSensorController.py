"""SH Controller Template controller."""

from controller import Robot
from controller import Supervisor


from config.definitions import CONFIG
from SHConnection.sh_connection import CONECTION
from SHDevices.sh_distance_sensor import *

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
sh_device = SH_Distance_Sensor(robot.getName(), connection=connection, device=robot)
sh_device.connect()


deltaTime = 0

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    deltaTime += timestep
    # check if messages are send from WebUI 
    sh_device.receive_webui(web_message_cb)

    # do something every 500ms
    if deltaTime > 500:
        deltaTime = 0
        sh_device.updateCurrentDistance()

        if sh_device.getDistance() <= sh_device.getTriggerDistance():
            sh_device.setTriggered(True)
        else:
            sh_device.setTriggered(False)
    pass

# cleanup on Exit
sh_device.log("---- CLEANUP ----")
sh_device.disconnect()