import sys
import os

from gsmmodem.modem import GsmModem, SentSms
from gsmmodem.exceptions import TimeoutException, PinRequiredError, IncorrectPinError

class SmsService(object):
	def __init__(self, address="/dev/ttyUSB0", baud=9600, pin=""):
		self.address = address
		self.pin = pin
		self.baud = baud
		self.modem = GsmModem(self.address, self.baud)

	def log(self, msg):
		print msg

	def connect(self):
		if not os.path.exists(self.address):
			return False
		self.log("Connecting to GSM modem")
		try:
			self.modem.connect(self.pin)
			self.modem.waitForNetworkCoverage(5)
			self.modem.smsTextMode = False 
			return True
		except PinRequiredError:
			self.log('Error: SIM card PIN required')
		except IncorrectPinError:
			self.log('Error: Incorrect SIM card PIN entered.\n')
		except TimeoutException:
			self.log('Error: Timeout.\n')
			self.close()
		return False

	def send(self, destination, text, waitForDeliveryReport=False):
		if not self.connect():
			return False
		try:
			sms = self.modem.sendSms(destination, text, waitForDeliveryReport=waitForDeliveryReport)
		except TimeoutException:
			self.log('Failed to send message: the send operation timed out')
			self.close()
		except Exception as e:
			self.log(e)
			self.close()
		else:
			self.close()
			if sms.report:
				return sms.status == SentSms.DELIVERED
		return False

	def close(self):
		self.modem.close()

