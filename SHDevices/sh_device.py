import json
from random import getstate
import struct
import threading, time
import websocket
import struct

from SHDevices.sh_state import *

class WebSocketClient(threading.Thread):

    def __init__(self, uri="ws://192.168.10.126:3000",
                            open_cb=None,
                            message_cb=None,
                            error_cb=None,
                            close_cb=None):
        self.uri = uri

        self.open_cb = open_cb
        self.message_cb = message_cb
        self.error_cb = error_cb
        self.close_cb = close_cb

        threading.Thread.__init__(self)
        self.port = 3000
        self.connected = False
        

    def is_connected(self):
        return self.connected

    def send(self,msg):
        try:
            self.server.send(json.dumps(msg))
            return True
        except Exception as e:
            print ("Sending Error: " + str(e))
            return False

    def on_message(self, ws, message):
        #print("WebSocket thread: %s" % message)
        try:
            msg = json.loads(message)
        except Exception as e:
            self.on_error(None,e)
        
            return
        if self.message_cb is not None:
            self.message_cb(ws,msg)

    def on_open(self, ws):
        #print("Connected!")
        self.connected = True
        if self.open_cb is not None:
            self.open_cb(ws)
    
    def on_close(self, ws, close_status_code, close_msg):
        #print("### closed ###")
        self.connected = False
        if self.close_cb is not None:
            self.close_cb(ws, close_status_code, close_msg)
    
    def on_error(self, ws, error):
        print(error)
        if self.error_cb is not None:
            self.error_cb(ws, error)
    
    def connect(self):
        self.server = websocket.WebSocketApp(self.uri,
                              on_open=self.on_open,
                              on_message=self.on_message,
                              on_error=self.on_error,
                              on_close=self.on_close)
        self.deamon = True
        self.start()
        pass

    def reconnect(self):
        print ("Retry : %s" % time.ctime())
        time.sleep(3)
        self.connect()

    def run(self):
        #print("Connecting to Websocket Server!")
        self.server.run_forever()

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

    def setStateValue(self, name, value):
        self.getState(name).setValue(value)
        self.sendState(self.getState(name))
    
    def register(self):
        self.log("REGISTER")
        self.sendObject()
        pass

    def connect(self):
        self.connection.connect()

    def reset(self):
        self.log("RESET") 

    # def set_SFColor(value):
    #     for n in range(len(value)):
    #         if value[n] != 0:
    #             value[n] = 1.0/value[n]]


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
        if msg:
            self.log("WebUI -> " + str(msg))
            if msg == "---- WINDOW LOADED ----":
                self.init_webui()
            else:
                try:
                    message = json.loads(msg)
                    callback(message)
                except Exception as e:
                    self.log("WebUIError" + str(e))
                    return
                
    def __str__(self):
        string = ""
        for key, value in self.states.items():
            string += key + ": " + str(value) +"\n"

        string += "\n"
        for key, value in self.fields.items() :
            string += key + ": " + str(value) +"\n"
        
        return string
