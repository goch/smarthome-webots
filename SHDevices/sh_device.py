import json
import struct
import threading
import websocket


class WebSocketClient(threading.Thread):

    def __init__(self, uri="ws://192.168.10.126:3000",
                            open_cb=None,
                            message_cb=None,
                            error_cb=None,
                            close_cb=None):

        self.open_cb = open_cb
        self.message_cb = message_cb
        self.error_cb = error_cb
        self.close_cb = close_cb

        threading.Thread.__init__(self)
        self.port = 3000
        self.connected = False
        self.server = websocket.WebSocketApp("ws://192.168.10.126:3000",
                              on_open=self.on_open,
                              on_message=self.on_message,
                              on_error=self.on_error,
                              on_close=self.on_close)

    def is_connected(self):
        return self.connected

    def send(self,msg):
        try:
            self.server.send(msg)
            return True
        except Exception as e:
            print ("Sending Error: " + str(e))
            return False
        

    def on_message(self, ws, message):
        #print("WebSocket thread: %s" % message)
        if self.message_cb is not None:
            self.message_cb(ws,message)

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

    def add_state(self, name, value):
        self.states[name] = value

    def add_field(self, name,value):
        self.fields[name] = value

    def setState(self, name,value):
        print("setState "+name+": " +str(value))
    
    def register(self):
        #send request to supervisor
        pass

    def reset(self):
        print ("reset: "+ self.name) 

    # def set_SFColor(value):
    #     for n in range(len(value)):
    #         if value[n] != 0:
    #             value[n] = 1.0/value[n]]

    def toJSON(self):
        return json.dumps({"name": self.name, "data": self.states})
    
    def send(self,message):
        if self.connection is not None:
            self.connection.send(message)
        else:
            self.log("Not Connected")
        
        if self.device is not None:
            self.device.wwiSendText(message)             


    def __str__(self):
        string = ""
        for key, value in self.states.items():
            string += key + ": " + str(value) +"\n"

        string += "\n"
        for key, value in self.fields.items() :
            string += key + ": " + str(value) +"\n"
        
        return string
