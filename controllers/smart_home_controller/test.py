from sh_device import SHDevice, RGBLight


global DDB

DDB ={}

rgbLamp = RGBLight("RGBLight")
DDB[rgbLamp.name] = rgbLamp
print(rgbLamp)

rgbLamp.set_state("r",1)
rgbLamp.set_state("g",1)
rgbLamp.set_state("b",1)
rgbLamp.set_state("brightness",1)
rgbLamp.set_state("on",True)
print(rgbLamp)

