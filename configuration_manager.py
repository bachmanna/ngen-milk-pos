from models import *
from pony.orm import commit, select

class ConfigurationManager:
	def __init__(self):
		pass

	def get(self, key):
		config = Configuration.get(key=key)
		if config: 
			return config.value 
		else: 
			return None

	def set(self, key, value):
		config = Configuration.get(key=key)
		if config:
			config.set(value=str(value))
		else:
			config = Configuration(key=key, value=str(value))
		commit()