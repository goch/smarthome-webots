#!/usr/bin/env python

import threading
import logging
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket


class WebsocketServer(WebSocket):

    def handleMessage(self):
        print (self.data)
        # echo message back to client
        self.sendMessage(self.data)

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')


class WebSocketThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.port = 3000
        self._logger = logging.getLogger(__name__)

    def run(self):
        #try:
            self._logger.info("Websocket Server started on port %s" % self.port)
            self.wsd = SimpleWebSocketServer('', self.port, WebsocketServer)
            self.wsd.serveforever()
        #except:
            self._logger.error("WebSocket Crash!")


