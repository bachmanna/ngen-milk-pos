import gobject
import gtk

from models import *
from configuration_manager import ConfigurationManager, ResourceFilesConstants


class BasicSetupUI:
    key_maps = {
        65457: "DateTimeSetupUI",
        65458: "TicketSettingsUI",
        65459: "SystemSettingsUI"
    }

    def __init__(self, parent):
        self.parent = parent
        self.builder = gtk.Builder()
        self.builder.add_from_file(ResourceFilesConstants.BASIC_SETUP_GLADE_FILE)
        self.builder.connect_signals(parent)
        self.container = self.builder.get_object("basicSetupContainer")
        self.parent.add(self.container)
        self.container.show()


    def handle_keypress(self, widget, data):
        print __name__, data.keyval

        if data.keyval in self.key_maps.keys():
            self.parent.change_page(self.key_maps[data.keyval])
            return True

        return False