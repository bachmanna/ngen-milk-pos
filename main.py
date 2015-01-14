#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

class MilkPOSLauncher:

    # This is a callback function. The data arguments are ignored
    # in this example. More on callbacks below.
    def hello(self, widget, data=None):
        print "Hello World"

    def delete_event(self, widget, event, data=None):
        # If you return FALSE in the "delete_event" signal handler,
        # GTK will emit the "destroy" signal. Returning TRUE means
        # you don't want the window to be destroyed.
        # This is useful for popping up 'are you sure you want to quit?'
        # type dialogs.
        print "delete event occurred"

        # Change FALSE to TRUE and the main window will not be destroyed
        # with a "delete_event".
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def __init__(self):
        # create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
    
        # Sets the border width of the window.
        self.window.set_border_width(10)
    
        # Creates a new button with the label "Hello World".
        self.button = gtk.Button("Hello World")
        self.button.connect("clicked", self.hello, None)
    
        # This will cause the window to be destroyed by calling
        # gtk_widget_destroy(window) when "clicked".  Again, the destroy
        # signal could come from here, or the window manager.
        self.button.connect_object("clicked", gtk.Widget.destroy, self.window)
    
        # This packs the button into the window (a GTK container).
        self.window.add(self.button)
    
        # The final step is to display this newly created widget.
        self.button.show()
    
        # and the window
        self.window.show()

    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()

def create_test_data():
    from services.member_service import MemberService
    mservice = MemberService()    
    name = "John"+str(random.randint(0,9999))
    mobile = str(random.randint(111111111,999999999))
    member_id = mservice.add(name=name, 
                            cattle_type=CattleType.COW, 
                            mobile=mobile)
    
    member = mservice.get(member_id)
    print member.id
    print member.name
    print member.cattle_type
    print member.mobile

    from services.milkcollection_service import MilkCollectionService
    collection = {}
    collection['member'] = member
    collection['shift'] = CollectionShift.MORNING
    collection['fat'] = 4.2
    collection['snf'] = 7.9
    collection['qty'] = 1.5
    collection['clr'] = 28.63
    collection['aw'] = 89.24
    collection['rate'] = 26.48
    collection['total'] = collection['rate'] * collection['qty']
    collection['created_by'] = 1

    colService = MilkCollectionService()
    col_id = colService.add(collection)

    col = colService.get(col_id)
    #print_collection(col)

    for x in colService.search(member_id=member_id):
        print_collection(x)

    from services.milksale_service import MilkSaleService
    saleService = MilkSaleService()
    sale_id = saleService.add(shift=CollectionShift.MORNING, 
                                qty=random.randint(1,5)*2.3, 
                                cattle_type=CattleType.BUFFALO,
                                rate=random.randint(1,5)*12.3,
                                created_by=1)
    sale = saleService.get(sale_id)
    #print_sale(sale)

    for x in saleService.search(_id=sale_id):
        print_sale(sale)


    # rate service test
    from services.rate_service import RateService
    rateService = RateService()
    rateService.set_cow_sale_rate(36.56)
    print "\n\nCow Sale Rate :", rateService.get_cow_sale_rate()

    rateService.set_buffalo_sale_rate(29.33)
    print "\nBuffalo Sale Rate :", rateService.get_buffalo_sale_rate()

def print_sale(sale):
    print "\n\n===========SALE================"
    print "\nId: ", sale.id
    print "\nShift: ", sale.shift
    print "\nCattle: ", sale.cattle_type
    print "\nQty: ", sale.qty
    print "\nRate: ", sale.rate
    print "\nTotal: ", sale.total

def print_collection(col):
    print "\n\n===========COLLECTION================"
    print "\nId: ", col.id
    print "\nShift: ", col.shift
    print "\nMember: ", col.member.name
    print "\nCattle: ", col.member.cattle_type
    print "\nQty: ", col.qty
    print "\nRate: ", col.rate
    print "\nTotal: ", col.total

# If the program is run directly or passed as an argument to the python
if __name__ == "__main__":
    from pony.orm import sql_debug, db_session
    from db_manager import db
    from models import *
    import random

    sql_debug(False)
    db.generate_mapping(create_tables=True)
    #db.drop_all_tables(with_all_data=True)
    #db.create_tables()

    with db_session:
        create_test_data()

    #launcher = MilkPOSLauncher()
    #launcher.main()