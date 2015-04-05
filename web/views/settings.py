from flask import render_template, request, redirect, g, flash, jsonify
from flask_login import login_required
from flask_babel import lazy_gettext
from dateutil.parser import parse
import sys
import os

from web import app

from configuration_manager import ConfigurationManager
from models.constants import *

@app.route("/basic_setup", methods=['GET', 'POST'])
@login_required
def basic_setup():
  if request.method == 'POST':
    settings = {}
    d = request.form.get("date", None)
    t = request.form.get("time", None)
    if d and t:
        try:
            dt = parse(d + " " + t)
            print dt
            if sys.platform == "linux2":
                os.system("sudo hwclock --set --date %s" % str(dt)) # set rtc hardware
                os.system("sudo hwclock -s") # copy to system
        except Exception as e:
            print "basic_setup", e
            flash(str(lazy_gettext("Invalid datetime value", "error")))
            return render_template("basic_setup.jinja2")

    settings[SystemSettings.SOCIETY_NAME] = request.form["society_name"]
    settings[SystemSettings.SOCIETY_ADDRESS] = request.form["society_address"]
    settings[SystemSettings.SOCIETY_ADDRESS1] = request.form["society_address1"]

    settings[SystemSettings.HEADER_LINE1] = request.form["header_line1"]
    settings[SystemSettings.HEADER_LINE2] = request.form["header_line2"]
    settings[SystemSettings.HEADER_LINE3] = request.form["header_line3"]
    settings[SystemSettings.HEADER_LINE4] = request.form["header_line4"]

    settings[SystemSettings.FOOTER_LINE1] = request.form["footer_line1"]
    settings[SystemSettings.FOOTER_LINE2] = request.form["footer_line2"]
    configManager = ConfigurationManager()
    configManager.set_all_settings(settings)
    return redirect("/")

  return render_template("basic_setup.jinja2")


@app.route("/settings", methods=['GET', 'POST'])
@login_required
def settings():
  if request.method == 'POST':
    configManager = ConfigurationManager()
    settings = {}
    settings[SystemSettings.SCALE_TYPE] = request.form["scale_type"]
    settings[SystemSettings.ANALYZER_TYPE] = request.form["analyzer_type"]
    settings[SystemSettings.RATE_TYPE] = request.form["rate_type"]
    settings[SystemSettings.COLLECTION_PRINTER_TYPE] = request.form["collection_printer"]
    settings[SystemSettings.DATA_EXPORT_FORMAT] = request.form["data_export_format"]

    settings[SystemSettings.MANUAL_FAT] = bool(request.form.get("manual_fat", False))
    settings[SystemSettings.MANUAL_SNF] = bool(request.form.get("manual_snf", False))
    settings[SystemSettings.MANUAL_QTY] = bool(request.form.get("manual_qty", False))
    settings[SystemSettings.PRINT_CLR] = bool(request.form.get("print_clr", False))
    settings[SystemSettings.PRINT_WATER] = bool(request.form.get("print_water", False))
    settings[SystemSettings.PRINT_BILL] = bool(request.form.get("print_bill", False))
    settings[SystemSettings.QUANTITY_2_DECIMAL] = bool(request.form.get("quantity_2_decimal", False))
    configManager.set_all_settings(settings)
    return redirect("/")

  return render_template("settings.jinja2")