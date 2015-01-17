import gtk

import pango

from configuration_manager import ConfigurationManager, ResourceFilesConstants

from models import *
import MainMenu


class PosMain:
    key_maps = {
        65360: "MainMenu",
        65470: "Collection",
        65472: "member_edit"
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

        MainMenu.MainMenu(self)


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


    def showWindow(self):
        self.window.show_all()
        self.window.fullscreen()

    def keypress(self, widget, data=None):
        mod = gtk.accelerator_get_label(data.keyval, data.state)
        print "This key was pressed ", data.keyval, mod
        if data.keyval in self.key_maps.keys():
            self.clean_bclabels()
            self.changePage(self.key_maps[data.keyval])

    def btnClicked(self, widget, data=None):
        name = gtk.Buildable.get_name(widget)
        if name and len(name) > 4:
            pageName = name[3:]
            self.changePage(pageName)

    def changePage(self, className):
        self.mainContainer.remove(self.currentPage)
        if className and len(className) > 0:
            m = __import__(className, globals(), locals(), className)
            c = getattr(m, className)
            c(self)

    def clean_bclabels(self):
        bc_label1 = self.builder.get_object("label1")
        bc_label2 = self.builder.get_object("label2")
        bc_label3 = self.builder.get_object("label3")
        bc_label1.set_text('')
        bc_label2.set_text('')
        bc_label3.set_text('')
