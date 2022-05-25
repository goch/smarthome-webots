import json
import struct

from SHDevices.sh_state import *


class SHDevice(object):

    def __init__(self, name, connection=None,device=None, states={}, fields={}):
        self.name = name
        self.device = device

        self.states = states
        self.fields = fields
        self.connection = connection

    def log(self, message):
        print(self.name + ": " + message)

    def add_state(self, name, value, min=None, max=None, type=None ):
        self.states[name] = SH_State(name=name, value=value, min=min, max=max, dataType=type )

    def add_field(self, name,value):
        self.fields[name] = value

    def getState(self,name):
        return self.states[name]

    def getStateValue(self,name):
        return self.getState(name).getValue()

    def setStateValue(self, name, value ,ignoreSame=True):        
        oldValue = self.getStateValue(name)    
        if ignoreSame == True or oldValue != value:
            self.getState(name).setValue(value)
            self.sendState(self.getState(name))
        # else: 
        #     self.log("NOT SENDING SAME VALUE: " + str(value))
    
    def register(self):
        self.log("REGISTER")
        self.sendObject()
        pass

    def connect(self):
        self.connection.connect()

    def disconnect(self):
        self.connection.disconnect()
    
    def reset(self):
        self.log("RESET") 

    def toDict(self):
        msg = {}
        msg["type"] = "object"
        msg["name"] = self.name

        data = {}

        for key, state in self.states.items():
            data[state.getName()] = state.toDict()

        msg["data"] = data
        return msg
    
    def send(self, message):
        # self.log(str(message))
        if self.connection is not None:
            self.connection.send(message)
        else:
            self.log("Not Connected")

        self.send_webui(message)

    def sendObject(self):
        data = self.toDict()
        # self.log("sendObject: " + str(data))
        self.send(data)
        pass

    def sendState(self,state):
        data = {}
        data["type"] = "state"
        data["name"] = self.name
        data["data"] = state.toDict(full=False)
        self.send(data)
        pass

    def sendReset(self):
        data = {}
        data["type"] = "reset"
        data["name"] = self.name
        self.send(data)
        pass

    def init_webui(self):
        self.send_webui(self.toDict())
    
    def send_webui(self,message):
        if self.device is not None:
            self.device.wwiSendText(json.dumps(message))
        else:
            self.log("webui not loaded"); 
            pass

    def receive_webui(self,callback):
        msg = self.device.wwiReceiveText()
        data = None
        if msg:
            if msg == "---- WINDOW LOADED ----":
                self.init_webui()
                return

            self.log("WebUI -> " + str(msg))
            try:
                data = json.loads(msg)
            except Exception as e:
                self.log("NOT JSON: " + str(e))
                
            callback(data)
                
    def __str__(self):
        string = ""
        for key, value in self.states.items():
            string += key + ": " + str(value) +"\n"

        string += "\n"
        for key, value in self.fields.items() :
            string += key + ": " + str(value) +"\n"
        
        return string
