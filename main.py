#!/usr/bin/env python

import pygtk

pygtk.require('2.0')
import gtk

from ui.settings import SettingsUI

class MilkPOSLauncher:

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file("resources/glade/home.glade")
        self.window = self.builder.get_object("mainWindow")
        self.lblKeyHints = self.builder.get_object("lblKeyHints")

        self.window.connect("destroy", self.destroy)
        self.window.connect('key-press-event', self.accelerator_keys)

        self.container = self.builder.get_object("mainContainer")
        SettingsUI(self.container, None)

        gtk.rc_parse("gtkrc-2.0.styles")
        screen = self.window.get_screen()
        settings = gtk.settings_get_for_screen(screen)
        gtk.rc_reset_styles(settings)

        self.window.fullscreen()
        self.window.show()


    def accelerator_keys(self, window, event):
        #key, mods = gtk.accelerator_parse("F10")
        keyval = event.keyval
        mod = gtk.accelerator_get_label(keyval, event.state)
        #print mod
        self.lblKeyHints.set_markup("<span size='xx-large'>%s   -- %d</span>" % (mod, keyval))
        pass

    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()


def create_test_data():
    from services.member_service import MemberService

    mservice = MemberService()
    name = "John" + str(random.randint(0, 9999))
    mobile = str(random.randint(111111111, 999999999))
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
    # print_collection(col)

    for x in colService.search(member_id=member_id):
        print_collection(x)

    from services.milksale_service import MilkSaleService

    saleService = MilkSaleService()
    sale_id = saleService.add(shift=CollectionShift.MORNING,
                              qty=random.randint(1, 5) * 2.3,
                              cattle_type=CattleType.BUFFALO,
                              rate=random.randint(1, 5) * 12.3,
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


def datetime_test():
    from datetime import datetime
    from helpers.datetime_util import set_system_datetime

    d = datetime.now()
    print "BEFORE:", d
    time_tuple = (d.year,  # Year
                  d.month,  # Month
                  d.day + 1,  # Day
                  d.hour,  # Hour
                  d.minute,  # Minute
                  d.second,  # Second
                  d.microsecond,  # Millisecond
    )
    set_system_datetime(time_tuple)
    d = datetime.now()
    print "AFTER:", d


def test_settings():
    from configuration_manager import ConfigurationManager

    configManager = ConfigurationManager()
    settings = {}
    settings[SystemSettings.SCALE_TYPE] = ScaleType.HEAVY
    settings[SystemSettings.ANALYZER_TYPE] = AnalyzerType.TVS
    settings[SystemSettings.RATE_TYPE] = CollectionRateType.FAT

    settings[SystemSettings.BILL_OVERWRITE] = True
    settings[SystemSettings.MANUAL_FAT] = True
    settings[SystemSettings.MANUAL_SNF] = True
    settings[SystemSettings.MANUAL_QTY] = True
    settings[SystemSettings.PRINT_CLR] = False
    settings[SystemSettings.PRINT_WATER] = False
    settings[SystemSettings.PRINT_BILL] = True
    settings[SystemSettings.QUANTITY_2_DECIMAL] = True
    settings[SystemSettings.EXTERNAL_DISPLAY] = False
    settings[SystemSettings.COLLECTION_PRINTER_TYPE] = "Thermal"

    configManager.set_all_settings(settings)

    settings = configManager.get_all_settings()
    for k in settings.keys():
        print k, " = ", settings[k]

# If the program is run directly or passed as an argument to the python
if __name__ == "__main__":
    from pony.orm import sql_debug, db_session
    from db_manager import db
    from models import *
    import random

    sql_debug(False)
    db.generate_mapping(create_tables=True)
    # db.drop_all_tables(with_all_data=True)
    #db.create_tables()

    with db_session:
        #create_test_data()
        #test_settings()

        #datetime_test()

        launcher = MilkPOSLauncher()
        launcher.main()