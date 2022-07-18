from SHConnection.iobroker_websocket import *

class ConnectionFactory:
    def __init__(self):
        self._builders = {}
        pass

    def register_builder(self, key, builder):
        self._builders[key] = builder

    def create(self, **kwargs):
        builder = self._builders.get(kwargs['type'])
        if not builder:
            raise ValueError(kwargs['type'])
        return builder(**kwargs)



CONECTION = ConnectionFactory()
CONECTION.register_builder('iobroker-websocket', iobroker_websocketBuilder())