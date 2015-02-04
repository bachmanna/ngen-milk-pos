import gtk

from models import *
from configuration_manager import ConfigurationManager, ResourceFilesConstants
from services.member_service import MemberService


class MemberSetupUI:

    def __init__(self, parent):
        self.parent = parent
        self.builder = gtk.Builder()
        self.builder.add_from_file(ResourceFilesConstants.MEMBER_SETUP_GLADE_FILE)
        self.container = self.builder.get_object("memberListContainer")

        self.load()

        self.parent.add(self.container)
        self.container.show()
        pass

    def save(self, obj):
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