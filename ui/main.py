import gtk
import pango

from configuration_manager import ConfigurationManager, ResourceFilesConstants
from models import *
from ui.MainMenuUI import MainMenuUI


class PosMain:
    key_maps = {
        65360: "MainMenuUI",
        65470: "CollectionUI",
        65471: "SalesUI",
        65472: "BasicSetupUI",
        65473: "SystemSetupUI",
        65474: "ReportsUI",
        65475: "DataResetUI",
    }

    def __init__(self):
        self.builder = gtk.Builder()
        self.currentPage = None

        config_manager = ConfigurationManager()
        settings = config_manager.get_all_settings()

        self.builder.add_from_file(ResourceFilesConstants.HOME_GLADE_FILE)
        self.builder.connect_signals(self)

        self.window = self.builder.get_object("mainWindow")
        self.window.connect('key-press-event', self.keypress)
        self.window.connect("destroy", self.destroy)

        # set logo
        logo = self.builder.get_object("imgLogo")
        logo.set_from_file(ResourceFilesConstants.LOGO_IMAGE_FILE)

        title = self.builder.get_object("lblCompanyName")
        address = self.builder.get_object("lblCompanyAddress")
        date = self.builder.get_object("lblDate")
        time = self.builder.get_object("lblTime")
        self.pageTitle = self.builder.get_object("pagetitle")

        title.set_text(settings[SystemSettings.SOCIETY_NAME])
        address.set_text(settings[SystemSettings.SOCIETY_ADDRESS])

        title.modify_font(pango.FontDescription("sans 48"))
        address.modify_font(pango.FontDescription("sans 28"))
        date.modify_font(pango.FontDescription("sans 16"))
        time.modify_font(pango.FontDescription("sans 16"))
        self.pageTitle.modify_font(pango.FontDescription("sans 20"))

        self.mainContainer = self.builder.get_object("mainContainer")
        self.change_app_theme(ResourceFilesConstants.GTK_THEME_FILE, self.window)

        self.currentPage = MainMenuUI(self)


    def change_app_theme(self, theme_rc_file, win):
        print theme_rc_file
        gtk.rc_set_default_files([theme_rc_file])
        gtk.rc_reparse_all_for_settings(gtk.settings_get_default(), True)
        gtk.rc_reset_styles(gtk.settings_get_for_screen(win.get_screen()))
        # gtk.rc_parse(theme_rc_file)
        # screen = self.window.get_screen()
        # settings = gtk.settings_get_for_screen(screen)
        # gtk.rc_reset_styles(settings)


    def destroy(self, widget, data=None):
        gtk.main_quit()


    def show_window(self):
        self.window.show_all()
        # self.window.fullscreen()

    def keypress(self, widget, data=None):
        mod = gtk.accelerator_get_label(data.keyval, data.state)
        print "This key was pressed ", data.keyval, mod
        if data.keyval in self.key_maps.keys():
            self.clean_bclabels()
            self.change_page(self.key_maps[data.keyval])

    def btnClicked(self, widget, data=None):
        name = gtk.Buildable.get_name(widget)
        page_name = name[3:]
        self.change_page(page_name)

    def change_page(self, class_name):
        module_name = "ui." + class_name
        m = __import__(module_name, globals(), locals(), class_name)
        c = getattr(m, class_name)

        if c != self.currentPage:
            self.currentPage = c
            self.clean_bclabels()
            self.clear_container()
            c(self)

    def clean_bclabels(self):
        bc_label1 = self.builder.get_object("label1")
        bc_label2 = self.builder.get_object("label2")
        bc_label3 = self.builder.get_object("label3")
        bc_label1.set_text('')
        bc_label2.set_text('')
        bc_label3.set_text('')

    def clear_container(self):
        for item in self.mainContainer.get_children():
            self.mainContainer.remove(item)

    def add(self, child):
        self.mainContainer.add(child)