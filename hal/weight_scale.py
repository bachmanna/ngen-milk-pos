import serial

address = "/dev/ttyUSB0"

scale_settings = {
			"OPAL": { "baud": 9600, "bytesize": serial.EIGHTBITS, "parity": serial.PARITY_NONE, "stopbits": serial.STOPBITS_TWO}, 
			"ISHATA": { "baud": 9600, "bytesize": serial.EIGHTBITS, "parity": serial.PARITY_NONE, "stopbits": serial.STOPBITS_TWO}, 
			"D-SONIC": { "baud": 9600, "bytesize": serial.EIGHTBITS, "parity": serial.PARITY_NONE, "stopbits": serial.STOPBITS_TWO}, 
			"SATHIYAM": { "baud": 9600, "bytesize": serial.EIGHTBITS, "parity": serial.PARITY_NONE, "stopbits": serial.STOPBITS_TWO}
			}

class WeightScale(object):
	def __init__(self, scale_type):
		settings = scale_settings[scale_type]
		try:
			self.scale = serial.Serial(address, settings["baud"])
			self.scale.bytesize = settings["bytesize"]
			self.scale.parity = settings["parity"]
			self.scale.stopbits = settings["stopbits"]

			self.scale.timeout = 3
			self.scale.xonxoff = False
			self.scale.rtscts = False
			self.scale.dsrdtr = False
		except Exception as e:
			print e

	def get(self):
		data = ""
		try:
			self.scale.open()
			data = self.scale.readline()
			self.scale.close()
		except Exception as e:
			print e
			from random import randint
			data = "L +000." + str(randint(100,999))
		if data[0] == 'L':
			return float(data[3:])
		return 0.0

	pass