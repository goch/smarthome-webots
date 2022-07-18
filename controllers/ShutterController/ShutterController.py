"""ShutterController controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
from controller import Supervisor

from config.definitions import CONFIG
from SHConnection.sh_connection import CONECTION

from SHDevices.sh_shutter import *





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

# create connection object
connection_config = CONFIG.getDeviceConnection(robot.getName())
connection  = CONECTION.create(key=connection_config['type'], **connection_config) 
connection.register_callbacks(connected, closed, error, message_cb)

shutter = SH_Shutter(robot.getName(),connection=connection,device=robot)
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

shutter.log("---- CLEANUP ----")
shutter.disconnect()