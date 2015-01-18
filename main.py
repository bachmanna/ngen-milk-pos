#!/usr/bin/env python
import os
import sys

pwd = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(pwd)

import pygtk

pygtk.require('2.0')
import gtk

from ui.main import PosMain


class MilkPOSLauncher:
    def __init__(self):
        self.pos = PosMain()


    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        self.pos.show_window()
        gtk.main()


# If the program is run directly or passed as an argument to the python
if __name__ == "__main__":
    from pony.orm import sql_debug, db_session
    from db_manager import db
    from models import *

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