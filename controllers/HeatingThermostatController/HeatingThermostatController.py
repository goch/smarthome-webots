"""SH Controller Template controller."""

from controller import Robot
from controller import Supervisor

from SHDevices.sh_heating_thermostat import *
from SHDevices.iobroker_websocket import *

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
sh_device = SH_Heating_Thermostat(robot.getName(), connection=ws, device=robot)
sh_device.connect()

heatup_intervall = 0 

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    

    # check if messages are send from WebUI 
    sh_device.receive_webui(web_message_cb)
    
    heatup_intervall += timestep
    
    # TODO: make heating system configurable
    # change temperature every 10s
    if heatup_intervall % (1 * 1000) == 0:
        heatup_intervall = 0
        currentTemp = sh_device.getCurrentTemperature()
        setTemp = sh_device.getSetTemperature()

        if currentTemp < setTemp:
            # TODO heatup configurable
            # TODO PID controller to controll heatup decision
            sh_device.updateCurrentTemperature(round(currentTemp + 0.1, 2))
        elif currentTemp > setTemp:
            sh_device.updateCurrentTemperature(round(currentTemp - 0.1, 2))
            pass
             
    
    pass

# cleanup on Exit
