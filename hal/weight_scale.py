import serial
from random import randint

scale_settings = {
			"OPAL": { "baud": 9600, "bytesize": serial.EIGHTBITS, "parity": serial.PARITY_NONE, "stopbits": serial.STOPBITS_TWO}, 
			"ISHATA": { "baud": 9600, "bytesize": serial.EIGHTBITS, "parity": serial.PARITY_NONE, "stopbits": serial.STOPBITS_TWO}, 
			"D-SONIC": { "baud": 9600, "bytesize": serial.EIGHTBITS, "parity": serial.PARITY_NONE, "stopbits": serial.STOPBITS_TWO}, 
			"SATHIYAM": { "baud": 9600, "bytesize": serial.EIGHTBITS, "parity": serial.PARITY_NONE, "stopbits": serial.STOPBITS_TWO}
			}

class WeightScale(object):
	def __init__(self, scale_type, address = "/dev/ttyUSB1"):
		settings = scale_settings[scale_type]
		self.scale = None
		try:
			self.scale = serial.Serial(address, settings["baud"], timeout=3)
			self.scale.bytesize = settings["bytesize"]
			self.scale.parity = settings["parity"]
			self.scale.stopbits = settings["stopbits"]

			self.scale.xonxoff = False
			self.scale.rtscts = False
			self.scale.dsrdtr = False
		except Exception as e:
			print "Err scale", e

	def get(self):
		data = " L +000." + str(randint(100,999))
		if self.scale:
			try:
				self.scale.open()
				self.scale.flushInput()
				self.scale.flushOutput()

				data = self.scale.readline()
				self.scale.close()
			except Exception as e:
				print "Err scale:", e
				data = "L +000." + str(randint(100,999))
		if data[1] == 'L':
			return float(data[4:])
		return 0.0

	pass