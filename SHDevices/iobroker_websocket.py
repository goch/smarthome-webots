import json
import threading, time
import websocket

class WebSocketClient(threading.Thread):

    def __init__(self, uri="ws://localhost:3000",
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
