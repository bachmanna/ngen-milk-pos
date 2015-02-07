import gtk

from configuration_manager import ResourceFilesConstants


class MainMenuUI:
    def __init__(self, parent):
        self.builder = gtk.Builder()
        self.builder.add_from_file(ResourceFilesConstants.MENU_GLADE_FILE)
        self.builder.connect_signals(parent)
        container = self.builder.get_object("mainmenu")

        mainBtnColor = "#4be3cf"
        secondBtnColor = "#e4f249"

        self.set_btn_color(self.builder.get_object("btnMainMenuUI"), mainBtnColor)
        # self.set_btn_color(self.builder.get_object("btnCollectionUI"), secondBtnColor)
        # self.set_btn_color(self.builder.get_object("btnSalesUI"), secondBtnColor)
        # self.set_btn_color(self.builder.get_object("btnBasicSetupUI"), secondBtnColor)
        # self.set_btn_color(self.builder.get_object("btnSystemSetupUI"), secondBtnColor)
        # self.set_btn_color(self.builder.get_object("btnReportsUI"), secondBtnColor)
        # self.set_btn_color(self.builder.get_object("btnDataResetUI"), secondBtnColor)

        parent.add(container)

    def set_btn_color(self, btn, color):
        btn.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(color))
        btn.modify_bg(gtk.STATE_ACTIVE, gtk.gdk.color_parse(color))
        btn.modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.color_parse(color))
        btn.modify_bg(gtk.STATE_SELECTED, gtk.gdk.color_parse(color))
        pass
