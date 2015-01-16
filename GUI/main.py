import pygtk
import gtk
import pango

class PosMain:
    """This is an Hello World GTK application"""

    def __init__(self):
        # Set the Glade file
        self.main_window = "../resources/glade/main_window.glade"
        self.homePageFile = "../resources/glade/homepage.glade"
        self.collectionPageFile = "../resources/glade/collectionpage.glade"
        self.builder = gtk.Builder()
        self.accel_group = gtk.AccelGroup()
        
        self.builder.add_from_file(self.main_window)
        self.builder.add_from_file(self.homePageFile)
        self.builder.add_from_file(self.collectionPageFile)
        
        self.window = gtk.Window()
        self.window.add_accel_group(self.accel_group)
        self.window.connect('key-press-event', self.keypress)
        self.header = self.builder.get_object("header")
        self.homePage = self.builder.get_object("homepage")
        self.collectionPage = self.builder.get_object("collectionpage")
        	
        
        color = gtk.gdk.color_parse('#aaf')
        color1 = gtk.gdk.color_parse('#333')
        
        title = self.builder.get_object("companyName")
        address = self.builder.get_object("companyAddress")
        title.modify_font(pango.FontDescription("sans 48"))
        address.modify_font(pango.FontDescription("sans 28"))
        
        self.pageTitle = self.builder.get_object("pagetitle")
        self.pageTitle.modify_font(pango.FontDescription("sans 20"))
        
        self.eb = gtk.EventBox()
        self.box = gtk.VBox()

        self.header = self.builder.get_object("header")
        
        self.eb.add(self.header)
        self.box.add(self.eb)
        self.eb.modify_bg(gtk.STATE_NORMAL, color)
        self.homePage.modify_bg(gtk.STATE_NORMAL, color1)
        
        if (self.window):
            self.window.connect("destroy", gtk.main_quit)

    def showWindow (self):
        self.box.add(self.homePage)
        self.window.add(self.box)
        self.builder.connect_signals(self)
        self.window.show_all()

    def collection (self, widget, data=None):
        self.box.remove(self.homePage)
        self.box.add(self.collectionPage)

    def mainMenu (self, widget, data=None):
        self.box.remove(self.collectionPage)
        self.box.add(self.homePage)

    def keypress(self, widget, data=None):
        print "this key was pressed" + str(data.keyval)
        if(data.keyval == 65470):
            self.mainMenu(self, widget)
        elif(data.keyval == 65471):
            self.collection(self, widget)

if __name__ == "__main__":
    pos = PosMain()
    pos.showWindow()
    gtk.main()
