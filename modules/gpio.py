#!/usr/bin/env python3
import re

GPIO_DIRECTORY='/sys/class/gpio'

class GPIOError(Exception):
    def __init__(self, message):
        super(GPIOError, self).__init__(message)

class GPIO:
    @property
    def pin(self):
        return self.__pin
    @pin.setter
    def pin(self, value):
        pass

    @property
    def port(self):
        return self.__port
    @port.setter
    def port(self, value):
        pass

    @property
    def number(self):
        return self.__number
    @number.setter
    def number(self, value):
        pass

    @property
    def address(self):
        return self.__address
    @address.setter
    def address(self, value):
        pass

    @property
    def direction(self):
        return self.__direction
    @direction.setter
    def direction(self, value):
        pass

    @property
    def value(self):
        return int(open(GPIO_DIRECTORY + '/gpio' + self.__address + '/value', 'r').read().strip())
    @value.setter
    def value(self, value):
        open(GPIO_DIRECTORY + '/gpio' + self.__address + '/value', 'w').write(str(value))

    def __init__(self, pin, direction='in'):
        try:
            self.__pin = pin.lower()
            regex = r'p(?P<port>[a-z])(?P<number>[0-9]*)'
            self.__port = re.match(regex, self.__pin).group('port')
            self.__number = int(re.match(regex, self.__pin).group('number'))
            self.__address = str(32*(ord(self.__port)-97) + self.__number)
        except:
            raise GPIOError('Invalid pin format!')
        if direction not in ('in', 'out'):
            raise GPIOError('Invalid direction!')
        self.__direction = direction
        open(GPIO_DIRECTORY + '/export', 'w').write(self.__address)
        open(GPIO_DIRECTORY + '/gpio' + self.__address + '/direction', 'w').write(self.__direction)
        self.value = 0

    def __del__(self):
        if self.direction == 'out':
            self.value = 0
        open(GPIO_DIRECTORY + '/unexport', 'w').write(self.__address)
