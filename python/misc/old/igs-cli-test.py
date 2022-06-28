#!/bin/python3
try:
    import RPi.GPIO as GPIO
    import pyfirmata
except:
    print('not on Pi')
from datetime import datetime
import sys
import argparse


whichswitch = sys.argv[1]
state = sys.argv[2]
numpump = sys.argv[3]

print(datetime.now().strftime("%H:%M - %m/%d/%Y"))
print("./this_file [device to control] [target state] [pump number]\nUser input was: ", sys.argv)

whichswitch = sys.argv[1]
state = sys.argv[2]
numpump = sys.argv[3]

GPIO.setmode(GPIO.BOARD)
GPIO.setup(37,GPIO.OUT)
GPIO.setup(40,GPIO.OUT)
GPIO.setup(38,GPIO.OUT)
print("GPIO set up")

board = pyfirmata.Arduino('/dev/ttyACM0')
print("Connected to arduino")

pump1 = board.digital[6]
pump2 = board.digital[7]
pump3 = board.digital[8]
pump4 = board.digital[9]
pump5 = board.digital[10]

pumps = [pump1, pump2, pump3, pump4, pump5]


def fan_toggle(state):
    if state:
        GPIO.output(37,GPIO.LOW)
    else:
        GPIO.output(37,GPIO.HIGH)

def led_upper(state):
    if GPIO.input(40):
        GPIO.output(40,GPIO.LOW)
    else:
        GPIO.output(40,GPIO.HIGH)

def led_lower(state):
    if GPIO.input(38):
        GPIO.output(38,GPIO.LOW)           
    else:
        GPIO.output(38,GPIO.HIGH)


class pump_toggle():
    def __init__(self, pumpstate, pump):
        self.pump_num = pumps[pump]
        try:
            self.state = bool(pumpstate)
            if self.state:
                self.pump_num.write(1)
            else:
                self.pump_num.write(1)
        except:
            print("Invalid pump state: ", self.pumpstate)


def main():
    if whichswitch == "fan":
        fan_toggle(int(sys.argv[2]))
    elif whichswitch == "upper":
        upper_toggle(int(sys.argv[2]))
    elif whichswitch == "lower":
        lower_toggle(int(sys.argv[2]))
    elif whichswitch == "pump":
        pump_toggle(int(sys.argv[2]), int(sys.argv[3]))
    else:
        print("Invalid arg 1: ", sys.argv[1])

main()