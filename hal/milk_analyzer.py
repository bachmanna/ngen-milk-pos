import serial

address = "/dev/ttyUSB0"

analyzer_settings = {
			"ULTRA": { "baud": 1200, "bytesize": serial.SEVENBITS, "parity": serial.PARITY_NONE, "stopbits": serial.STOPBITS_TWO}, 
			"ULTRA_PRO": { "baud": 2400, "bytesize": serial.EIGHTBITS, "parity": serial.PARITY_NONE, "stopbits": serial.STOPBITS_TWO}, 
			"LACTO_SCAN": { "baud": 9600, "bytesize": serial.EIGHTBITS, "parity": serial.PARITY_NONE, "stopbits": serial.STOPBITS_TWO}, 
			"KSHEERA": { "baud": 9600, "bytesize": serial.EIGHTBITS, "parity": serial.PARITY_NONE, "stopbits": serial.STOPBITS_TWO}
			}

class MilkAnalyzer(object):
	def __init__(self, scale_type):
		settings = analyzer_settings[scale_type]
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
		s = ""
		result = { "fat": 0.0 , "snf": 0.0, "water": 0.0, "clr": 0.0 }
		try:
			self.scale.open()
			self.scale.flushInput()
			self.scale.flushOutput()

			i = 0
			data = []
			while True:
				i = i + 1
				d = self.scale.read()
				if d == '(':
					data = []
				data.append(d)
				if d == ')':
					s = ''.join([ str(x) for x in data])
					break
				if i > 100:
					break
			     
			self.scale.close()
		except Exception as e:
			print e
			from random import randint
			f = randint(1000,1200)
			s = randint(1000,1200)
			w = randint(5000,9999)
			c = randint(6000,9999)
			s = "(%d%d%d%d0000)" % (f,s,w,c)
		print s
		if s[0] == '(':
			result["fat"] = float(s[1:3] +"." + s[3:5])
			result["snf"] = float(s[5:7] +"." + s[7:9])
			result["water"] = float(s[9:11] +"." + s[11:13])
			result["clr"] = float(s[13:15] +"." + s[15:17])
		return result

	pass