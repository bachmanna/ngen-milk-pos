import pygtk
import gtk
import pango
from datetime import datetime
from configuration_manager import ConfigurationManager
from models import *
import MainMenu


class PosMain:
    """This is an Hello World GTK application"""

    def __init__(self):
        # Set the Glade file
        self.mainWindowFile = "resources/glade/home.glade"
        self.builder = gtk.Builder()
        self.currentPage = None

        config_manager = ConfigurationManager()
        settings = config_manager.get_all_settings()

        self.builder.add_from_file(self.mainWindowFile)

        self.window = self.builder.get_object("mainWindow")
        self.window.connect('key-press-event', self.keypress)

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
        MainMenu.MainMenu(self)

        self.width, self.height = self.window.get_size()

    def showWindow(self):
        self.builder.connect_signals(self)
        self.window.show_all()
        self.window.fullscreen()

    def keypress(self, widget, data=None):
        print "this key was pressed" + str(data.keyval)
        if data.keyval in self.accelMap.keys():
            self.changePage(self.accelMap[data.keyval])

    def btnClicked(self, widget, data=None):
        name = gtk.Buildable.get_name(widget)
        pageName = name[3:]
        self.changePage(pageName)

    def changePage(self, className):
        self.mainContainer.remove(self.currentPage)
        m = __import__(className, globals(), locals(), className)
        c = getattr(m, className)
        c(self)

