import pygtk
import gtk
import pango
from services.member_service import MemberService
from services.milkcollection_service import MilkCollectionService
from models import *

import os

pwd = os.path.dirname(__file__)
resource_dir = os.path.join(pwd, "../resources/glade/")


class Collection:
    """This is an Hello World GTK application"""

    def __init__(self, PosMain):
        newPageFile = resource_dir + "collectionpage.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(newPageFile)
        self.builder.connect_signals(self)
        newPage = self.builder.get_object("collectionpage")
        self.m_code = self.builder.get_object("Emcode")
        self.m_service = MemberService()
        bc_label1 = PosMain.builder.get_object("label1")
        self.shift = CollectionShift.MORNING
        if self.shift == "M":
            shift_label = "Morning Shift"
        else:
            shift_label = "Evening Shift"
        bc_label1.set_text(shift_label)
        bc_label1.modify_font(pango.FontDescription("sans 16"))

        bc_label2 = PosMain.builder.get_object("label2")
        lbl_new = "New - N"
        bc_label2.set_text(lbl_new)
        bc_label3 = PosMain.builder.get_object("label3")
        lbl_print = "Print - P"
        bc_label3.set_text(lbl_print)

        PosMain.mainContainer.add(newPage)
        PosMain.pageTitle.set_text("Collection")
        PosMain.currentPage = newPage
        self.builder.get_object("Erate").set_text('20.0')
        self.m_code.grab_focus()

    def get_member_details(self, widget, data=None):
        m_code = widget.get_text()
        self.m_details = self.m_service.get(int(m_code))
        m_name = self.builder.get_object("lblMName")
        m_name.modify_font(pango.FontDescription("sans 16"))
        m_cattle = self.builder.get_object("lblCattle")
        m_cattle.modify_font(pango.FontDescription("sans 16"))

        m_name.set_text(self.m_details.name)
        m_cattle.set_text(self.m_details.cattle_type)
        self.change_focus(widget)

    def change_focus(self, widget, data=None):
        widget.get_toplevel().child_focus(gtk.DIR_TAB_FORWARD)

    def save_data(self, widget, data=None):
        collection = {}
        collection['member'] = self.m_details
        collection['shift'] = self.shift
        collection['fat'] = float(self.builder.get_object("Efat").get_text())
        collection['snf'] = float(self.builder.get_object("Esnf").get_text())
        collection['qty'] = float(self.builder.get_object("Eqty").get_text())
        collection['clr'] = float(self.builder.get_object("Eclr").get_text())
        collection['aw'] = float(self.builder.get_object("Eaw").get_text())
        collection['rate'] = float(self.builder.get_object("Erate").get_text())
        collection['total'] = float(
            self.builder.get_object("Eamount").get_text())  # collection['rate'] * collection['qty']
        collection['created_by'] = 1

        colService = MilkCollectionService()
        col_id = colService.add(collection)
        #self.m_code.grab_focus()

    def clear_data(self, widget, data=None):
        self.m_code.set_text('')
        self.builder.get_object("Efat").set_text('')
        self.builder.get_object("Esnf").set_text('')
        self.builder.get_object("Eqty").set_text('')
        self.builder.get_object("Eclr").set_text('')
        self.builder.get_object("Eaw").set_text('')
        self.builder.get_object("Eamount").set_text('')
        self.m_code.grab_focus()

    def focus_save(self, widget, data=None):
        btnSave = self.builder.get_object("btnSave")
        total = self.builder.get_object("Eamount")
        qty = float(self.builder.get_object("Eqty").get_text())
        rate = float(self.builder.get_object("Erate").get_text())
        total_amount = qty * rate
        total.set_text(str(total_amount))
        btnSave.grab_focus()

    def keypress(self, widget, data=None):
        data_keyval = data.keyval
        if (data_keyval == ord("n")):
            self.clear_data(widget)
        elif (data_keyval == ord("p")):
            pass
            # TO DO: Print


