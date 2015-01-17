import pygtk
import gtk
import pango
from datetime import datetime

class PosMain:
    """This is an Hello World GTK application"""

    def __init__(self):
        # Set the Glade file
        self.headerFile = "resources/glade/header.glade"
        self.homePageFile = "resources/glade/mainmenu.glade"
        #self.collectionPageFile = "resources/glade/collectionpage.glade"
        self.builder = gtk.Builder()
        self.accelMap = {65470:"mainmenu",65471:"collectionpage"}
        
        self.builder.add_from_file(self.headerFile)
        self.builder.add_from_file(self.homePageFile)
        #self.builder.add_from_file(self.collectionPageFile)
        
        self.window = gtk.Window()
        self.window.connect('key-press-event', self.keypress)
        self.header = self.builder.get_object("header")
        self.mainmenuPage = self.builder.get_object("mainmenu")
        #self.collectionPage = self.builder.get_object("collectionpage")
        	
        
        headerColor = gtk.gdk.color_parse('#aaf')
        bodyColor = gtk.gdk.color_parse('#fff')
        btnColor = gtk.gdk.color_parse('#ffff00')
        
        title = self.builder.get_object("companyName")
        address = self.builder.get_object("companyAddress")
        title.modify_font(pango.FontDescription("sans 48"))
        address.modify_font(pango.FontDescription("sans 28"))
        
        self.pageTitle = self.builder.get_object("pagetitle")
        self.pageTitle.modify_font(pango.FontDescription("sans 20"))
        
        self.btnCollection = self.builder.get_object("btnCollection")
        self.btnCollection.modify_bg(gtk.STATE_NORMAL, btnColor)
        
        self.btnSales = self.builder.get_object("btnSales")
        self.btnSales.modify_bg(gtk.STATE_NORMAL, btnColor)
        
        self.btnBasicSetting = self.builder.get_object("btnBasicSetting")
        self.btnBasicSetting.modify_bg(gtk.STATE_NORMAL, btnColor)
        
        self.btnsysSetting = self.builder.get_object("btnsysSetting")
        self.btnsysSetting.modify_bg(gtk.STATE_NORMAL, btnColor)
        
        self.btnReports = self.builder.get_object("btnReports")
        self.btnReports.modify_bg(gtk.STATE_NORMAL, btnColor)
        
        self.btnDataReset = self.builder.get_object("btnDataReset")
        self.btnDataReset.modify_bg(gtk.STATE_NORMAL, btnColor)
        
        self.headerBox = gtk.EventBox()
        self.bodyBox = gtk.EventBox()
        self.box = gtk.VBox()
        footer = gtk.Label()
        footer.set_text(str(datetime.now()))
        self.box.pack_end(footer)

        self.header = self.builder.get_object("header")
        
        self.headerBox.add(self.header)
        self.bodyBox.add(self.mainmenuPage)
        self.currentPage = self.mainmenuPage
        
        self.box.add(self.headerBox)
        self.box.add(self.bodyBox)
        self.width, self.height = self.window.get_size()
        
        self.headerBox.modify_bg(gtk.STATE_NORMAL, headerColor)
        self.header.set_size_request(self.width,int(self.height*0.035))
        self.bodyBox.modify_bg(gtk.STATE_NORMAL, bodyColor)
        self.mainmenuPage.set_size_request(self.width,int(self.height*0.95))
        footer.set_size_request(self.width,3)
        
        
        if (self.window):
            self.window.connect("destroy", gtk.main_quit)

    def showWindow (self):
        self.window.add(self.box)
        self.builder.connect_signals(self)
        self.window.show_all()
        self.window.fullscreen()

    def collection (self, widget, data=None):
        self.changePage(self.collectionPage)

    def mainMenu (self, widget, data=None):
        self.changePage(self.mainmenuPage)

    def keypress(self, widget, data=None):
        print "this key was pressed" + str(data.keyval)
        if data.keyval in self.accelMap.keys():
            self.changePage(self.accelMap[data.keyval])
    
    def changePage(self, gladeFileName):
        self.bodyBox.remove(self.currentPage)
        newPageFile = "resources/glade/"+gladeFileName+".glade"
        builder = gtk.Builder()
        builder.add_from_file(self.newPageFile)
        newPage = self.builder.get_object(gladeFileName)
        self.bodyBox.add(newPage)
        self.currentPage = newPage
        #self.currentPage.set_size_request(self.width,int(self.height*0.99))

