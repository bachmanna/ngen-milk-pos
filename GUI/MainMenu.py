import pygtk
import gtk
import pango

import os

pwd = os.path.dirname(__file__)
resource_dir = os.path.join(pwd, "../resources/glade/")


class MainMenu:
    """This is an Hello World GTK application"""

    def __init__(self, PosMain):
        newPageFile = resource_dir + "mainmenu.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(newPageFile)
        self.builder.connect_signals(PosMain)
        newPage = self.builder.get_object("mainmenu")
        PosMain.mainContainer.add(newPage)
        PosMain.pageTitle.set_text("Main Menu")
        PosMain.currentPage = newPage


