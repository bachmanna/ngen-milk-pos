from flask import render_template, request, redirect, g, flash, url_for
from flask_login import login_required
from flask_babel import lazy_gettext, gettext

try:
    from collections import OrderedDict
except ImportError:
    # python 2.6 or earlier, use backport
    from ordereddict import OrderedDict
from random import random

from web import app, fmtDecimal, get_backup_directory

from services.rate_service import RateService
from services.export_import_service import ExportImportService
from models import *


@app.route("/rate_setup", methods=['GET', 'POST'])
@login_required
def rate_setup():
  return render_template("rate_setup.jinja2")


@app.route("/rate_fat", methods=['GET', 'POST'])
@login_required
def rate_fat():
  cattle_type = request.args.get("cattle_type", "COW")
  rate_service = RateService()

  if request.method == 'POST':
    id = int(request.form.get("id", 0))
    cattle_type = request.form.get("cattle_type", "COW")
    min_value = request.form.get("min_value", "0.0")
    min_value = request.form.get("min_value", "0.0")
    max_value = request.form.get("max_value", "0.0")
    rate = request.form.get("rate", "0.0")
    if min_value and max_value and rate:
      min_value = float(min_value)
      max_value = float(max_value)
      rate = float(rate)
      rate_service.update_fat_collection_rate(cattle_type,id,min_value,max_value,rate)
      flash("Rate data saved successfully!")
    else:
      flash("Invalid data!", category="error")

  rate_list = rate_service.get_fat_collection_rate(cattle_type=cattle_type)
  return render_template("rate_fat.jinja2", cattle_type=cattle_type, rate_list=rate_list,rate_type="fat")


@app.route("/rate_fat_and_snf", methods=['GET', 'POST'])
@login_required
def rate_fat_and_snf():
  cattle_type = request.args.get("cattle_type", "COW")
  rate_service = RateService()

  if request.method == 'POST':
    try:
      fat = float(request.form.get("fat", 0.0))
      snf = float(request.form.get("snf", 0.0))
      rate = float(request.form.get("rate", 0.0))
      cattle_type = request.form.get("cattle_type", "COW")
      rate_service.save_fat_and_snf_collection_rate(cattle_type=cattle_type,fat_value=fat,snf_value=snf,rate=rate)
      flash("Rate data saved successfully!")
    except Exception as e:
      print e
      flash("Invalid data!", category="error")

  rate_list = rate_service.get_fat_and_snf_collection_rate(cattle_type=cattle_type)

  snf_list = set()
  rates = OrderedDict()
  for x in rate_list:
    snf_list.add(x.snf_value)
    if not x.fat_value in rates.keys():
      rates[x.fat_value] = {}
    rates[x.fat_value][x.snf_value] = x.rate
  snf_list = sorted(snf_list)
  return render_template("rate_fat_and_snf.jinja2", cattle_type=cattle_type, rate_list=rate_list, snf_list=snf_list, rates=rates, rate_type="fat_and_snf")


@app.route("/rate_total_solid", methods=['GET', 'POST'])
@login_required
def rate_total_solid():
  cattle_type = request.args.get("cattle_type", "COW")
  rate_service = RateService()

  if request.method == 'POST':
    try:
      data = {}
      id = int(request.form.get("id", 0))
      cattle_type = request.form.get("cattle_type", cattle_type)
      data["min_fat"] = float(request.form.get("min_fat", 0.0))
      data["max_fat"] = float(request.form.get("max_fat", 0.0))
      data["fat_rate"] = float(request.form.get("fat_rate", 0.0))
      data["min_snf"] = float(request.form.get("min_snf", 0.0))
      data["max_snf"] = float(request.form.get("max_snf", 0.0))
      data["snf_rate"] = float(request.form.get("snf_rate", 0.0))
      rate_service.save_ts1_collection_rate(id=id, cattle_type=cattle_type, data=data)
      flash("Rate data saved successfully!")
    except Exception as e:
      print e
      flash("Invalid data!", category="error")

  rate_list = rate_service.get_ts1_collection_rate(cattle_type=cattle_type)
  return render_template("rate_total_solid.jinja2", cattle_type=cattle_type, rate_list=rate_list,rate_type="ts1")


@app.route("/rate_total_solid1", methods=['GET', 'POST'])
@login_required
def rate_total_solid1():
  cattle_type = request.args.get("cattle_type", "COW")
  rate_service = RateService()

  if request.method == 'POST':
    try:
      id = int(request.form.get("id", 0))
      cattle_type = request.form.get("cattle_type", cattle_type)
      min_value = float(request.form.get("min_value", 0.0))
      max_value = float(request.form.get("max_value", 0.0))
      rate = float(request.form.get("rate", 0.0))
      rate_service.save_ts2_collection_rate(cattle_type,id,min_value,max_value,rate)
      flash("Rate data saved successfully!")
    except Exception as e:
      print e
      flash("Invalid data!", category="error")

  rate_list = rate_service.get_ts2_collection_rate(cattle_type=cattle_type)
  return render_template("rate_total_solid1.jinja2", cattle_type=cattle_type, rate_list=rate_list,rate_type="ts2")


@app.route("/rate_export")
@login_required
def rate_export():
  page = request.args.get("page", None)
  rate_type = request.args.get("rate_type", None)
  if not page or not rate_type:
    return redirect(url_for("rate_setup"))
  if do_export(rate_type):
    flash(str(lazy_gettext("Export successfull!")))
  else:
    flash(str(lazy_gettext("Import failed!")), "error")
  return redirect("/" + page)


@app.route("/rate_import")
@login_required
def rate_import():
  page = request.args.get("page", None)
  rate_type = request.args.get("rate_type", None)
  if not page or not rate_type:
    return redirect(url_for("rate_setup"))
  if do_import(rate_type):
    flash(str(lazy_gettext("Import successfull!")))
  else:
    flash(str(lazy_gettext("Import failed!")), "error")
  return redirect("/" + page)



map_rate_type_table = { "fat": FATCollectionRate.__table__,
                        "fat_and_snf": FATAndSNFCollectionRate.__table__,
                        "ts1": TS1CollectionRate.__table__,
                        "ts2": TS2CollectionRate.__table__
                      }

def do_export(rate_type):
  if not rate_type in map_rate_type_table.keys():
    return False
  table = map_rate_type_table[rate_type]
  service = ExportImportService(table)
  return service.do_export()


def do_import(rate_type):
  if not rate_type in map_rate_type_table.keys():
      return False
  table = map_rate_type_table[rate_type]
  service = ExportImportService(table)
  return service.do_import()