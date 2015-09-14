import serial
from random import randint

analyzer_settings = {
			"ULTRA": { "baud": 2400, "bytesize": serial.SEVENBITS, "parity": serial.PARITY_NONE, "stopbits": serial.STOPBITS_TWO}, 
			"ULTRA_PRO": { "baud": 2400, "bytesize": serial.SEVENBITS, "parity": serial.PARITY_NONE, "stopbits": serial.STOPBITS_TWO}, 
			"LACTO_SCAN": { "baud": 2400, "bytesize": serial.SEVENBITS, "parity": serial.PARITY_NONE, "stopbits": serial.STOPBITS_TWO}, 
			"KSHEERA": { "baud": 2400, "bytesize": serial.SEVENBITS, "parity": serial.PARITY_NONE, "stopbits": serial.STOPBITS_TWO}
			}

class MilkAnalyzer(object):
	def __init__(self, scale_type, address="/dev/ttyUSB0"):
		settings = analyzer_settings[scale_type]
		self.scale = None
		try:
			self.scale = serial.Serial(address, settings["baud"], timeout=10)
			self.scale.bytesize = settings["bytesize"]
			self.scale.parity = settings["parity"]
			self.scale.stopbits = settings["stopbits"]

			self.scale.xonxoff = False
			self.scale.rtscts = False
			self.scale.dsrdtr = False
		except Exception as e:
			print "Err milk analyzer", e

	def get_rand_values(self):
		f = randint(1000,1200)
		s = randint(1000,1200)
		w = randint(5000,9999)
		c = randint(6000,9999)
		s = "(%d%d%d%d00000000)" % (f,s,w,c)
		return s

	def get(self):
		s = "" #self.get_rand_values()
		result = { "fat": 0.0 , "snf": 0.0, "water": 0.0, "clr": 0.0 }
		if self.scale:
			try:
				self.scale.open()
				self.scale.flushInput()
				self.scale.flushOutput()

				i = 0
				data = []
				while True:
					i = i + 1
					d = self.scale.read()
					data.append(d)
					if d == ')':
						s = ''.join([str(x) for x in data])
						data = []
						i = 0
						if s[0] == '(':
							break
					if i > 100:
						break
				     
				self.scale.close()
			except Exception as e:
				print "Err milk analyzer", e

		if s and len(s) > 0 and s[0] == '(' and len(s) > 17:
			result["fat"] = float(s[1:3] +"." + s[3:5])
			result["snf"] = float(s[5:7] +"." + s[7:9])
			result["water"] = float(s[9:11] +"." + s[11:13])
			result["clr"] = float(s[13:15] +"." + s[15:17])
		return result

	pass