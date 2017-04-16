#!/usr/bin/env python
import os, time
DIR = "/sys/class/gpio"

def map( port ):
	map = {
		"PG00":{"name":"gpio9_pg0",   "number":9},
		"PG01":{"name":"gpio7_pg1",   "number":7},
		"PG02":{"name":"gpio8_pg2",   "number":8},
		"PG04":{"name":"gpio6_pg4",   "number":6},
		"PG05":{"name":"gpio5_pg5",   "number":5},
		"PG06":{"name":"gpio4_pg6",   "number":4},
		"PG07":{"name":"gpio19_pg7",  "number":19},
		"PG08":{"name":"gpio18_pg8",  "number":18},
		"PG09":{"name":"gpio17_pg9",  "number":17},
		"PG10":{"name":"gpio16_pg10", "number":16},
		"PG11":{"name":"gpio15_pg11", "number":15}
	}
	if not port in map:
		raise GPIOError("Port not found in mapping")
	return map[port]
	
def _open(port, direction, **args):
	## Check input arguments
	if not direction in ["in", "out"]:
		raise AttributeError("Invalid port direction (" + direction + ")")
	## Open the port with /export file
	data = map(port)
	if os.path.exists(DIR + "/" + data["name"]):
		raise GPIOError("Port is already opened")
	open(DIR + "/export", "w").write(str(data["number"]))
	## Write port direction with /<port>/direction file
	if not os.path.exists(DIR + "/" + data["name"]):
		raise GPIOError("Port can't be opened")
	open(DIR + "/" + data["name"] + "/direction", "w").write(direction)
	## Poll for rising or falling edges
	if direction=="in" and ("rise" in args or "fall" in args):
		while os.path.exists(DIR + "/" + data["name"]):
			value = _read(port)
			time.sleep(0.001)						## Sleep for 1ms
			if value=="0" and _read(port)=="1" and "rise" in args:
				args["rise"](port)
			elif value=="1" and _read(port)=="0" and "fall" in args:
				args["fall"](port)

def _close(*ports):
	## Close the ports with /unexport file
	for port in ports:
		try:
			data = map(port)
			if not os.path.exists(DIR + "/" + data["name"]):
				raise GPIOError("Port is already closed")
			open(DIR + "/unexport", "w").write(str(data["number"]))
		except:
			pass
			
def _read(port):
	data = map(port)
	if not os.path.exists(DIR + "/" + data["name"]):
		raise GPIOError("Port is not opened")
	if open(DIR + "/" + data["name"] + "/direction", "r").read().strip()!="in":
		raise GPIOError("Port is not defined as input")
	return open(DIR + "/" + data["name"] + "/value", "r").read().strip()

def _write(port, value):
	## Check input arguments
	if not value in ["0", "1"]:
		raise AttributeError("Invalid port value (" + value + ")")
	data = map(port)
	if not os.path.exists(DIR + "/" + data["name"]):
		raise GPIOError("Port is not opened")
	if open(DIR + "/" + data["name"] + "/direction", "r").read().strip()!="out":
		raise GPIOError("Port is not defined as output")
	open(DIR + "/" + data["name"] + "/value", "w").write(value)

class GPIOError(Exception):
	def __init__(self, message):
		super(GPIOError, self).__init__(message)
