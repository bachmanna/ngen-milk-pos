import pygtk
import gtk
import pango

import os

pwd = os.path.dirname(__file__)
resource_dir = os.path.join(pwd, "../resources/glade/")

class Collection:
    """This is an Hello World GTK application"""

    def __init__(self, PosMain):
        newPageFile =  resource_dir + "collectionpage.glade"
        builder = gtk.Builder()
        builder.add_from_file(newPageFile)
        newPage = builder.get_object("collectionpage")
        PosMain.mainContainer.add(newPage)
        PosMain.pageTitle.set_text("Collection")
        PosMain.currentPage = newPage



