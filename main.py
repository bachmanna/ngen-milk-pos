#!/usr/bin/env python
import os
import sys
from configuration_manager import ResourceFilesConstants

pwd = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(pwd)

import pygtk
from ui.member_list import MemberListUI

pygtk.require('2.0')
import gtk

from GUI.main import PosMain


class MilkPOSLauncher:
    def __init__(self):
        self.pos = PosMain()
<<<<<<< HEAD
        self.pos.showWindow()
        self.pos.accelMap = {65470:"MainMenu", 65471:"Collection", 65472:"MemberList"}
        self.pos.window.connect("destroy", self.destroy)
        self.changeTheme(self.GTK_THEME_FILE, self.pos.window)

    def old(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file(MilkPOSLauncher.HOME_GLADE_FILE)
        self.window = self.builder.get_object("mainWindow")
        self.lblKeyHints = self.builder.get_object("lblKeyHints")

        self.window.connect("destroy", self.destroy)
        self.window.connect('key-press-event', self.accelerator_keys)

        self.container = self.builder.get_object("mainContainer")
        logo = self.builder.get_object("imgLogo")
        logo.set_from_file(MilkPOSLauncher.LOGO_IMAGE_FILE)

        # SettingsUI(self.container, None)
        #TicketSettingsUI(self.container, None)
        MemberListUI(self.container, None)

        self.changeTheme(MilkPOSLauncher.GTK_THEME_FILE)
        self.window.show()
        self.window.fullscreen()

    def changeTheme(self, theme_rc_file, win):
        gtk.rc_set_default_files([theme_rc_file])
        gtk.rc_reparse_all_for_settings(gtk.settings_get_default(), True)
        gtk.rc_reset_styles(gtk.settings_get_for_screen(win.get_screen()))
        # gtk.rc_parse(theme_rc_file)
        #screen = self.window.get_screen()
        #settings = gtk.settings_get_for_screen(screen)
        #gtk.rc_reset_styles(settings)

    def accelerator_keys(self, window, event):
        # key, mods = gtk.accelerator_parse("Alt L + F10")
        keyval = event.keyval
        mod = gtk.accelerator_get_label(keyval, event.state)
        print mod, keyval
        self.lblKeyHints.set_markup("<span size='xx-large'>%s   -- %d</span>" % (mod, keyval))
        if keyval == 65479:
            self.destroy(self.window)
        elif keyval == 65360:
            # show menu
            pass
=======
>>>>>>> refactored some code in main.py

    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        self.pos.showWindow()
        gtk.main()


# If the program is run directly or passed as an argument to the python
if __name__ == "__main__":
    from pony.orm import sql_debug, db_session
    from db_manager import db
    from models import *
    import random

    sql_debug(False)
    db.generate_mapping(create_tables=True)
    # db.drop_all_tables(with_all_data=True)
    # db.create_tables()

    with db_session:
        from test_data import TestData

        test = TestData()
        #test.create_members()
        #test.test_settings()

        #test.datetime_test()

        launcher = MilkPOSLauncher()
        launcher.main()