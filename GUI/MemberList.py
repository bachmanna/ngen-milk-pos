import pygtk
import gtk
import pango
from services.member_service import MemberService

import os

pwd = os.path.dirname(__file__)
resource_dir = os.path.join(pwd, "../resources/glade/")


class MemberList:
    """This is an Hello World GTK application"""

    def __init__(self, PosMain):
        newPageFile = resource_dir + "member_list.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(newPageFile)
        self.builder.connect_signals(self)
        newPage = self.builder.get_object("memberListContainer")
        PosMain.mainContainer.add(newPage)
        PosMain.pageTitle.set_text("Member List")
        PosMain.currentPage = newPage
        self.load()

    def load(self):
        member_service = MemberService()
        lst = member_service.search()
        store = gtk.ListStore(self.builder.get_object("gridMember").get_model())
        store = gtk.ListStore(int, str, str, str)
        store.clear()
        for item in lst:
            store.append([item.id, item.name, item.cattle_type, item.mobile])
        self.builder.get_object("gridMember").set_model(store)