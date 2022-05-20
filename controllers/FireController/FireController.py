"""SH Controller Template controller."""

from controller import Robot
from controller import Supervisor

import struct

def getTF():
    global robot
    return robot.getSelf().getField("translation").getSFVec3f() 

def setTF(x,y,z):
    robot.getSelf().getField("translation").setSFVec3f([x,y,z]) 

def getSize():
    global robot
    return robot.getSelf().getField("size").getSFFloat()

def setSize(size):
    global robot
    robot.getSelf().getField("size").setSFFloat(size)

def getMaxSize():
    global robot
    return robot.getSelf().getField("maxSize").getSFFloat()

def getGrowth():
    global robot
    return robot.getSelf().getField("growth").getSFFloat()


#def getSize():
    #return robot.getSelf().getField("children").getMFNode(0).getField('geometry').getSFNode().getField('radius').getSFFloat()
#    return robot.getSelf().getField("size").getSFFloat()

def emitt(state):
    global emitter
    tf = getTF() 
    msg = struct.pack("?ddd",state,tf[0],tf[1],tf[2])
    emitter.send(msg)




TIME_STEP = 64
robot = Supervisor()
timestep = int(robot.getBasicTimeStep())

deltaTime = 0

emitter = robot.getDevice("emitter")
        
scale_max = getMaxSize()
scale_increment = getGrowth()


setSize(0.1)

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    deltaTime += timestep
    # check if messages are send from WebUI 

    scale = getSize()
    if scale < scale_max:
        size = scale + scale_increment
        print ("scale -> " + str(scale) + " inc: " + str(scale_increment) + " new: " + str(size))
        setSize(size)



    # do something every 500ms
    # if deltaTime > 500:
    #     deltaTime = 0
    #     sh_device.log("Hello World -> " + str(deltaTime))

    pass

# cleanup on Exit
