import gtk
from configuration_manager import ResourceFilesConstants


class SystemSetupUI:
    key_maps = {
        65457: "MemberSetupUI",
        65458: "RateSetupUI",
        65459: "PrinterSetupUI",
        65460: "UserSetupUI",
    }

    def __init__(self, parent):
        self.parent = parent
        self.builder = gtk.Builder()
        self.builder.add_from_file(ResourceFilesConstants.SYSTEM_SETUP_GLADE_FILE)
        self.builder.connect_signals(parent)
        self.container = self.builder.get_object("systemSetupContainer")
        self.parent.add(self.container)
        self.container.show()


    def handle_keypress(self, widget, data):
        print __name__, data.keyval

        if data.keyval in self.key_maps.keys():
            self.parent.change_page(self.key_maps[data.keyval])
            return True

        return False