import pygtk
import gtk
import pango
from datetime import datetime

class PosMain:
    """This is an Hello World GTK application"""

    def __init__(self):
        # Set the Glade file
        self.mainWindowFile = "resources/glade/home.glade"
        self.homePageFile = "resources/glade/mainmenu.glade"
        self.builder = gtk.Builder()
        
        self.builder.add_from_file(self.mainWindowFile)
        self.builder.add_from_file(self.homePageFile)
        
        self.window = self.builder.get_object("mainWindow")
        self.window.connect('key-press-event', self.keypress)
        self.mainmenuPage = self.builder.get_object("mainmenu")
        
        title = self.builder.get_object("lblCompanyName")
        address = self.builder.get_object("lblCompanyAddress")
        date = self.builder.get_object("lblDate")
        time = self.builder.get_object("lblTime")
        self.pageTitle = self.builder.get_object("pagetitle")
        
        title.modify_font(pango.FontDescription("sans 48"))
        address.modify_font(pango.FontDescription("sans 28"))
        date.modify_font(pango.FontDescription("sans 16"))
        time.modify_font(pango.FontDescription("sans 16"))
        self.pageTitle.modify_font(pango.FontDescription("sans 20"))
        
        self.mainContainer = self.builder.get_object("mainContainer")
        self.mainContainer.add(self.mainmenuPage)
        self.currentPage = self.mainmenuPage
        
        self.width, self.height = self.window.get_size()

    def showWindow (self):
        self.builder.connect_signals(self)
        self.window.show_all()
        self.window.fullscreen()

    def collection (self, widget, data=None):
        self.changePage("collection")

    def mainMenu (self, widget, data=None):
        self.changePage("mainmenu")

    def keypress(self, widget, data=None):
        print "this key was pressed" + str(data.keyval)
        if data.keyval in self.accelMap.keys():
            print self.accelMap[data.keyval]
            self.changePage(self.accelMap[data.keyval])
    
    def changePage(self, gladeFileName):
        self.mainContainer.remove(self.currentPage)
        newPageFile = "resources/glade/"+gladeFileName+".glade"
        print newPageFile
        builder = gtk.Builder()
        builder.add_from_file(newPageFile)
        newPage = builder.get_object(gladeFileName)
        self.mainContainer.add(newPage)
        self.pageTitle.set_text(gladeFileName)
        self.currentPage = newPage

