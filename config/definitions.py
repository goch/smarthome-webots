import os
import yaml

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

_CFG = yaml.load(open(os.path.join(ROOT_DIR, 'config', 'config.yaml'), 'r'), Loader=yaml.FullLoader)

class CONFIG(object):
    @staticmethod
    def getValue(key):
        try:
            return _CFG[key]
        except Exception as e:
            print(e)
    
    @staticmethod
    def getDeviceConfig(name):
        return CONFIG.getValue(name)

    @staticmethod
    def getDeviceConnection(name):
        try:
            connName = _CFG[name]['connection']
            return CONFIG.getValue(connName) 
        except Exception as e:
            print( name +": device specific connection not found. Loading default connection")
            connName = CONFIG.getValue('connection')
            return CONFIG.getValue(connName)
        
        


    

