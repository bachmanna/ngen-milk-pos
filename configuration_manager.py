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
        self._set_no_commit(key, value)
        commit()

    def _set_no_commit(self, key, value):
        config = Configuration.get(key=key)
        if config:
            config.set(value=str(value))
        else:
            config = Configuration(key=key, value=str(value))

    def get_scale_type(self):
        return self.get(SystemSettings.SCALE_TYPE)

    def set_scale_type(self, value):
        return self.set(SystemSettings.SCALE_TYPE, value)

    def get_analyzer_type(self):
        return self.get(SystemSettings.ANALYZER_TYPE)

    def set_analyzer_type(self, value):
        return self.set(SystemSettings.ANALYZER_TYPE, value)

    def get_rate_type(self):
        return self.get(SystemSettings.RATE_TYPE)

    def set_rate_type(self, value):
        return self.set(SystemSettings.RATE_TYPE, value)

    def get_all_settings(self):
        settings = {}
        for x in SystemSettings._get_keys():
            settings[x] = self.get(x)
        return settings

    def set_all_settings(self, settings):
        for x in settings.keys():
            if x in SystemSettings._get_keys():
                self._set_no_commit(x, settings[x])
        commit()