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
