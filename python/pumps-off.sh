#!/bin/bash
python -c "from pyfirmata import Arduino;board=Arduino('/dev/ttyACM0');[board.digital[i].write(0) for i in range(6,11)]"
