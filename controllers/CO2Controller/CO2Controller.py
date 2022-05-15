"""SH Controller Template controller."""

from os import times
from controller import Robot
from controller import Supervisor

from SHDevices.sh_device import *
from SHDevices.sh_co2_sensor import *

import json
from math import sqrt, pow
from config.definitions import ROOT_DIR, _CFG


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
sh_device = SH_CO2_Sensor(robot.getName(), connection=ws, device=robot)
sh_device.connect()

sensor_intervall = 0

receiver = robot.getDevice("receiver")
receiver.enable(timestep)

window_open_count = 0

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:

    sensor_intervall += timestep
    
    # TODO: make heating system configurable
    # measure data every 10s
    if sensor_intervall % 1000 == 0:
        sensor_intervall = 0
        

        # check if WINDOW send OPEN/CLOSE
        if receiver.getQueueLength() > 0:
            msg = receiver.getData()
            data = struct.unpack("?ddd",msg)
            # sh_device.log(str(data))
        
            sensor_pos = sh_device.getTransform()
            
            # check if window is open
            if getDistance(sensor_pos[0],sensor_pos[1],data[1],data[2]) < sh_device.sensor_range:
                sh_device.log(str(data[0]))
                if data[0] == True:  
                    window_open_count +=1
                elif window_open_count > 0:
                    window_open_count -=1
                
                receiver.nextPacket()

        humans = sh_device.device.getFromDef("HUMAN")
        # sh_device.log(str(type(humans)))
        # human_name = humans.getField("name").getSFString()
        
        co2_level = sh_device.getCO2Concentration()
        # there is a human
        if humans is not None:
            human_pos = humans.getField("translation").getSFVec3f()
            sensor_pos = sh_device.getTransform()
            # sh_device.log(human_name + "-> " + str(human_pos))
            # sh_device.log(str(sensor_pos))
                       
            distance = getDistance(sensor_pos[0],sensor_pos[1], human_pos[0],human_pos[1])

            # if human in range increase co2
            if distance <= sh_device.sensor_range:
                co2_level += 10
            pass    
 
         # decrease co2 if windows open     
        co2_level -= 10 * window_open_count               
        sh_device.updateCO2Concentration(co2_level)    


    # check if messages are send from WebUI 
    sh_device.receive_webui(web_message_cb)
    pass

# cleanup on Exit
