from db_manager import db
from models import *
import os

pwd = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))

from services.cache_manager import settings_cache as cache


class ResourceFilesConstants:
    BG_IMAGE_FILE = pwd + "/resources/icons/bg.png"
    MENU_GLADE_FILE = pwd + "/resources/glade/mainmenu.glade"
    HOME_GLADE_FILE = pwd + "/resources/glade/home.glade"
    LOGO_IMAGE_FILE = pwd + "/resources/icons/logo.png"

    COLLECTION_GLADE_FILE = pwd + "/resources/glade/collection.glade"
    SALES_GLADE_FILE = pwd + "/resources/glade/sales.glade"
    BASIC_SETUP_GLADE_FILE = pwd + "/resources/glade/basic_setup.glade"
    SYSTEM_SETUP_GLADE_FILE = pwd + "/resources/glade/system_setup.glade"
    REPORTS_GLADE_FILE = pwd + "/resources/glade/reports.glade"
    DATA_RESET_GLADE_FILE = pwd + "/resources/glade/data_reset.glade"
    SYSTEM_SETTINGS_GLADE_FILE = pwd + "/resources/glade/system_settings.glade"
    TICKET_SETTINGS_GLADE_FILE = pwd + "/resources/glade/ticket_settings.glade"
    MEMBER_SETUP_GLADE_FILE = pwd + "/resources/glade/member_list.glade"

    TICKET_TEMPLATE_THERMAL_FILE = "resources/ticket/ticket_template_thermal.txt"

    GTK_THEME_FILE = pwd + "/resources/CandidoCandy/gtkrc"
    # GTK_THEME_FILE = pwd + "/resources/DarkOrange/gtkrc"

    def __init__(self):
        pass


class ConfigurationManager:
    def __init__(self):
        pass

    def get(self, key):
        config = Configuration.query.filter_by(key=key).first()
        if config:
            return config.value
        else:
            return None

    def set(self, key, value):
        self._set_no_commit(key, value)
        db.session.commit()

    def _set_no_commit(self, key, value):
        config = Configuration.query.filter_by(key=key).first()
        if config:
            config.value = str(value)
        else:
            config = Configuration(key=key, value=str(value))
        db.session.add(config)

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
        def get_data():
            settings = {}
            for x in SystemSettings._get_keys():
                settings[x] = self.get(x)
            return settings
        data = cache.get(key="settings", createfunc=get_data)
        return data

    def set_all_settings(self, settings):
        cache.remove_value(key="settings")
        for x in settings.keys():
            if x in SystemSettings._get_keys():
                self._set_no_commit(x, settings[x])
        db.session.commit()