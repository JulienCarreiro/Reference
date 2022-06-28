import logging
import os
from time import sleep

computer = os.uname()[1]                    # current computer hostname - uname -n
homedir = os.environ['HOME']                # users home directory - $HOME

#sub process
#os.system('firefox')
#subprocess.call('firefox')

#replace current process
#os.execv('/bin/xfce4-terminal', [' ', 'top'])

try:
    print(bob)
except Exception as e:
    logging.error(e)

