import gtk

from models import *
from configuration_manager import ConfigurationManager
from services.member_service import MemberService


class MemberListUI:

    def __init__(self, parent, navigate):
        self.navigate = navigate
        self.parent = parent
        self.builder = gtk.Builder()
        self.builder.add_from_file("resources/glade/member_list.glade")
        self.container = self.builder.get_object("memberListContainer")

        self.load()

        self.parent.add(self.container)
        self.container.show()
        pass

    def save(self, obj):
        self.destroy()

    def destroy(self):
        if self.navigate:
            self.navigate.back()
        pass

    def load(self):
        member_service = MemberService()
        lst = member_service.search()
        #store = gtk.ListStore(self.builder.get_object("gridMember").get_model())
        store = gtk.ListStore(int, str, str, str)
        store.clear()
        for item in lst:
            store.append([item.id, item.name, item.cattle_type, item.mobile])
        self.builder.get_object("gridMember").set_model(store)