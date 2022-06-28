import pingo
from pyfirmata import Arduino

rpiboard = pingo.rpi.RaspberryPi
print("Connected to RPI")

inoboard = Arduino('/dev/ttyACM0')
print("Connected to arduino")

switches = [rpiboard.pins[i] for i in [37, 40, 38]]
pumps = [inoboard.digital[i] for i in [6, 7, 8, 9, 10]]

for switch in switches:
    pin.mode = pingo.OUT

for pump in range(5):
    pumps[pump].write(0)

switches[0].hi()
switches[1].lo()

pumps[0].write(0)