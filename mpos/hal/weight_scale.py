import serial
from random import randint

scale_settings = {
			"OPAL": { "baud": 9600, "bytesize": serial.EIGHTBITS, "parity": serial.PARITY_NONE, "stopbits": serial.STOPBITS_TWO, "tare": "T"}, 
			"ISHATA": { "baud": 9600, "bytesize": serial.EIGHTBITS, "parity": serial.PARITY_NONE, "stopbits": serial.STOPBITS_TWO, "tare": "T"}, 
			"D-SONIC": { "baud": 9600, "bytesize": serial.EIGHTBITS, "parity": serial.PARITY_NONE, "stopbits": serial.STOPBITS_TWO, "tare": "T"}, 
			"SATHIYAM": { "baud": 9600, "bytesize": serial.EIGHTBITS, "parity": serial.PARITY_NONE, "stopbits": serial.STOPBITS_TWO, "tare": "T"}
			}

class WeightScale(object):
	def __init__(self, scale_type, address = "/dev/ttyUSB1", qty2decimal=False):
		self.qty2decimal = qty2decimal == "True"
		self.scale_type = scale_type
		settings = scale_settings[scale_type]
		self.settings = settings
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

	def get_rand_values(self):
		data = " L +%3.3d.%3.3d" % (randint(1,10), randint(100,999))
		return data

	def get(self):
		value = 0.0
		data = "" # self.get_rand_values()
		if self.scale:
			try:
				self.scale.open()
				self.scale.flushInput()
				self.scale.flushOutput()

				data = self.scale.readline()
				self.scale.close()
			except Exception as e:
				print "Err scale:", e

		if data and len(data) > 1:
			if data[1] == 'L':
				value = float(data[4:])
			if data[1] == 'W':
				value = float(data[4:])/1.033

		if self.qty2decimal:
			value = float("%.2f" % (value))
		else:
			value = float("%.1f" % (value))

		return value

	def tare(self):
		tare_cmd = self.settings["tare"]
		if self.scale and tare_cmd:
			try:
				self.scale.open()
				self.scale.flushInput()
				self.scale.flushOutput()

				self.scale.write(tare_cmd)
				self.scale.close()
				return True
			except Exception as e:
				print "Err scale:", e
		return False
	pass