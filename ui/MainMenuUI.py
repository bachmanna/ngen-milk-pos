import gtk

from configuration_manager import ResourceFilesConstants


class MainMenuUI:
    def __init__(self, parent):
        self.builder = gtk.Builder()
        self.builder.add_from_file(ResourceFilesConstants.MENU_GLADE_FILE)
        self.builder.connect_signals(parent)
        container = self.builder.get_object("mainmenu")
        parent.add(container)
        parent.pageTitle.set_text("Main Menu")
