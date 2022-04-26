import json
import struct
class SHDevice(object):

    def __init__(self, name, device=None, emitter=None, receiver=None, states={}, fields={}):
        self.device = device  
        self.name = name
        self.emitter = emitter
        self.receiver = receiver
        self.states = states
        self.fields = fields

    def add_state(self, name, value):
        self.states[name] = value

    def add_field(self, name,value):
        self.fields[name] = value

    def set_state(self, name,value):
        print("setState "+name+": " +str(value))
    
    def register(self):
        #send request to supervisor
        message = {}
        message["type"] = "register"
        message["name"] = self.name
        msg = json.dumps(message)
        print("-- Sending Message! --")
        print(msg)
        
        try:
            self.emitter.send(msg.encode("utf-8"))
        except Exception as e:
            print("Error sending Message: "+ str(e))
        #wait for supervisor to assign comunication channel
        #self.receiver.enable(100)# check for messages each 100ms
    
    def setReceiveChannel(self, channel):
        self.receiver.setChannel(channel)


    def reset(self):
        print ("reset:"+name) 

    # def set_SFColor(value):
    #     for n in range(len(value)):
    #         if value[n] != 0:
    #             value[n] = 1.0/value[n]]

    def toJSON(self):
        return json.dumps({"name": self.name, "data": self.states})
    

    def __str__(self):
        string = ""
        for key, value in self.states.items():
            string += key + ": " + str(value) +"\n"

        string += "\n"
        for key, value in self.fields.items() :
            string += key + ": " + str(value) +"\n"
        
        return string
