"""ShutterController controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
from controller import Supervisor



import struct
from sh_shutter import *
from sh_device import *
from sh_shutter import *



TIME_STEP = 64
# create the Robot instance.
robot = Supervisor()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getDevice('motorname')
#  ds = robot.getDevice('dsname')
#  ds.enable(timestep)

emitter = robot.getDevice("emitter")
receiver = robot.getDevice("receiver")
receiver.enable(100)

shutter = SH_Shutter(robot.getName(),robot,emitter,receiver)
shutter.register()


# motor = robot.getDevice("linear motor")
# motor.setPosition(1.3)
# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    while receiver.getQueueLength() > 0:
        
        print( robot.getName() + ": -- DATA PACKET RECEIVED! --")
        msg = receiver.getData()
        print(msg)
        
        
        #if robot.getName() == "SH_SHUTTER":      
        #receiver.nextPacket()

    pass

