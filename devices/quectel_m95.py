#!/usr/bin/env python3
import time
import serial
import datetime

try:
    from modules.gpio import GPIO
except:
    pass

LOGFILE = '/root/_/logs/devices_quectel_m95.log'

def timestamp():
    return '[' + datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ") + ']'

class M95:
    @property
    def status(self):
        return self.STU.value
    @status.setter
    def status(self, value):
        pass

    def __init__(self):
        self.PWR = GPIO('pg1', 'out')
        self.STU = GPIO('pi3')
        self.PWR.value = 0

    def power_on(self, log = False):
        if log:
            open(LOGFILE, 'a').write(timestamp() + ' Turning on...\n')
        while not self.STU.value:
            self.PWR.value = 1
        self.PWR.value = 0
        time.sleep(1)
        if log:
            open(LOGFILE, 'a').write(timestamp() + ' Module turned on!\n')

    def power_off(self, log = False):
        if log:
            open(LOGFILE, 'a').write(timestamp() + ' Turning off...\n')
        while self.STU.value:
            self.PWR.value = 1
        self.PWR.value = 0
        time.sleep(1)
        if log:
            open(LOGFILE, 'a').write(timestamp() + ' Module turned off!\n')

    def reset(self):
        open(LOGFILE, 'a').write(timestamp() + ' Restart module...\n')
        self.power_off()
        self.power_on()
        open(LOGFILE, 'a').write(timestamp() + ' Module ready!\n')

if __name__=="__main__":
    import os
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from modules.gpio import GPIO

    if len(sys.argv)==3 and sys.argv[1]=='--send':
        open(LOGFILE, 'a').write(timestamp() + ' <- ' + sys.argv[2] + '\n')
    elif len(sys.argv)==2 and sys.argv[1]=='--power-off':
        M95().power_off(True)
        os.popen('systemctl stop quectel-m95.service').read().strip()
    else:
        M95().reset()
        s = serial.Serial('/dev/ttyS7', 9600, timeout=1)
        while True:
            line = ''
            last = os.popen('tail -1 ' + LOGFILE).read().strip()
            if 'Z] <- AT' in last:
                s.write((last[26:] + '\n').encode('ascii'))
                time.sleep(0.5)
                while line != last[26:]:
                    line = s.readline().decode('ascii').strip()
            line = s.readline().decode('ascii').strip()
            if not line:
                continue
            open(LOGFILE, 'a').write(timestamp() + ' -> ' + line + '\n')
