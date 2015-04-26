from flask import render_template, request, redirect, g, flash, url_for, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from flask_babel import lazy_gettext, gettext

from web import app, settings_provider, get_backup_directory, send_to_thermal_printer

from services.member_service import MemberService
from services.rate_service import RateService
from services.milkcollection_service import MilkCollectionService
from models import *

import os
import sys
#import xhtml2pdf.pisa as pisa

from flask_weasyprint import HTML, CSS

styles = None

def do_print_report(template, outfile, **kwargs):
  global styles
  bakdir = get_backup_directory()
  printer_type = request.args.get("printer_type", "usb")

  if printer_type == "thermal":
    print "Printing to thermal printer"
    tmp = app.jinja_env.get_template("thermal/" + template)
    data = settings_provider() or {}
    data.update(**kwargs)
    html = tmp.render(data)
    send_to_thermal_printer(html)
  else:
    dest = os.path.join(bakdir, outfile)
    print "Print pdf report to %s" % dest
    tmp = app.jinja_env.get_template("reports/" + template)
    data = settings_provider() or {}
    data.update(**kwargs)
    html = tmp.render(data)

    if styles is None:
      app_css = CSS(url_for("static", filename="css/app.css"))
      custom_css = CSS(url_for("static", filename="css/custom.css"))
      print_css = CSS(url_for("static", filename="css/print.css"))
      styles = [app_css,custom_css,print_css]

    HTML(string=html).write_pdf(target=dest, stylesheets=styles)
    
    if printer_type == "laser":
      print "Printing to laser printer."
      # send the pdf to CUPS

    if sys.platform == "win32":
      import xhtml2pdf.pisa as pisa
      #pisa.startViewer(dest)

@app.route("/reports")
@login_required
def reports():
  return render_template("reports.jinja2")


@app.route("/member_list")
@login_required
def report_member_list():
  member_service = MemberService()
  member_list = member_service.search()
  cow_member_list = [x for x in member_list if x.cattle_type == "COW"]
  buffalo_member_list = [x for x in member_list if x.cattle_type == "BUFFALO"]

  data = dict(member_list=member_list,cow_member_list=cow_member_list,buffalo_member_list=buffalo_member_list)

  if request.args.get("print", "False") == "True":
    do_print_report("member_list.jinja2", "member_list.pdf", **data)
    return jsonify({"success": True})

  return render_template("member_list.jinja2", **data)


@app.route("/absence_list")
@login_required
def absence_list():
  shift = request.args.get("shift", "MORNING")
  today = datetime.now().date()
  day   = int(request.args.get("day", today.day))
  month = int(request.args.get("month", today.month))
  year  = int(request.args.get("year", today.year))
  search_date = datetime(year, month, day).date()

  if search_date > today:
    search_date = today
    flash(str(lazy_gettext("Date cannot be greater than today!")), "error")

  collectionService = MilkCollectionService()
  lst = collectionService.search(created_at=search_date, shift=shift)

  member_service = MemberService()
  member_list = member_service.search()

  absence_members = []
  mids = [x.member_id for x in lst]
  for x in member_list:
    if not x.id in mids:
      absence_members.append(x)

  cow_member_list = [x for x in absence_members if x.cattle_type == "COW"]
  buffalo_member_list = [x for x in absence_members if x.cattle_type == "BUFFALO"]

  data = dict(member_list=absence_members,cow_member_list=cow_member_list,buffalo_member_list=buffalo_member_list,search_date=search_date,shift=shift)

  if request.args.get("print", "False") == "True":
    do_print_report("absence_list.jinja2", "absence_list.pdf", **data)
    return jsonify({"success": True})

  return render_template("absence_list.jinja2", **data)


@app.route("/detail_shift")
@login_required
def report_detail_shift():
  shift = request.args.get("shift", "MORNING")
  today = datetime.now().date()
  day   = int(request.args.get("day", today.day))
  month = int(request.args.get("month", today.month))
  year  = int(request.args.get("year", today.year))
  search_date = datetime(year, month, day).date()

  if search_date > today:
    search_date = today
    flash(str(lazy_gettext("Date cannot be greater than today!")), "error")

  collectionService = MilkCollectionService()
  members, mcollection, summary = collectionService.get_milk_collection_and_summary(shift, search_date)

  data = dict(mcollection=mcollection, member_list=members, summary=summary, search_date=search_date, shift=shift)

  if request.args.get("print", "False") == "True":
    do_print_report("detail_shift.jinja2", "detail_shift.pdf", **data)
    return jsonify({"success": True})

  return render_template("detail_shift.jinja2", **data)


@app.route("/shift_summary")
@login_required
def report_shift_summary():
  shift = request.args.get("shift", "MORNING")
  today = datetime.now().date()
  day   = int(request.args.get("day", today.day))
  month = int(request.args.get("month", today.month))
  year  = int(request.args.get("year", today.year))
  search_date = datetime(year, month, day).date()

  if search_date > today:
    search_date = today
    flash(str(lazy_gettext("Date cannot be greater than today!")), "error")

  collectionService = MilkCollectionService()
  members, mcollection, summary = collectionService.get_milk_collection_and_summary(shift, search_date)

  data = dict(mcollection=mcollection, member_list=members, summary=summary, search_date=search_date, shift=shift)

  if request.args.get("print", "False") == "True":
    do_print_report("shift_summary.jinja2", "shift_summary.pdf", **data)
    return jsonify({"success": True})

  return render_template("shift_summary.jinja2", **data)


@app.route("/payment_report")
@login_required
def payment_report():
  increment = float(request.args.get("increment", 0.0))
  end = datetime.now().date()
  start = end - timedelta(days=7)

  day   = int(request.args.get("from_day", start.day))
  month = int(request.args.get("from_month", start.month))
  year  = int(request.args.get("from_year", start.year))
  from_date = datetime(year, month, day).date()

  day   = int(request.args.get("to_day", end.day))
  month = int(request.args.get("to_month", end.month))
  year  = int(request.args.get("to_year", end.year))
  to_date = datetime(year, month, day).date()

  if to_date > end:
    to_date = end
    flash(str(lazy_gettext("To Date cannot be greater than today!")), "error")

  if to_date < from_date:
    to_date = end
    from_date = start
    flash(str(lazy_gettext("From Date cannot be greater than to date!")), "error")

  collectionService = MilkCollectionService()
  col_lst = collectionService.search_by_date(member_id=None,from_date=from_date,to_date=to_date)
  lst = {}
  summary = {"qty": 0.0, "rate": 0, "amount": 0, "increment": 0, "total": 0}

  if len(col_lst) > 0:
    member_service = MemberService()
    mlst = member_service.search()
    member_list = {}
    for x in mlst:
      member_list[x.id] = x

    for x in col_lst:
      if not x.member_id in lst.keys():
        inc = x.qty * increment
        total = x.total + inc
        lst[x.member_id] = { "name": member_list[x.member_id].name,
                             "qty": x.qty, "rate": x.rate, 
                             "fat": x.fat, "snf": x.snf, 
                             "amount": x.total, "increment": inc, "total": total}
      else:
        item = lst[x.member_id]
        item["qty"] = item["qty"] + x.qty
        item["rate"] = item["rate"] + x.rate
        item["fat"] = item["fat"] + x.fat
        item["snf"] = item["snf"] + x.snf
        item["amount"] = item["amount"] + x.total
        item["increment"] = item["qty"] * increment
        item["total"] = item["amount"] + item["increment"]
      item = lst[x.member_id]
      summary["qty"] = summary["qty"] + item["qty"]
      summary["amount"] = summary["amount"] + item["amount"]
      summary["increment"] = summary["increment"] + item["increment"]
      summary["total"] = summary["total"] + item["total"]

    summary["fat"] = "%.2f" % (sum([x.fat * x.qty for x in col_lst])/summary["qty"])
    summary["snf"] = "%.2f" % (sum([x.snf * x.qty for x in col_lst])/summary["qty"])
    summary["rate"] = "%.2f" % (sum([x.rate * x.qty for x in col_lst])/summary["qty"])

  data = dict(from_date=from_date,to_date=to_date,lst=lst,increment=increment,summary=summary)

  if request.args.get("print", "False") == "True":
    do_print_report("payment_report.jinja2", "payment_report.pdf", **data)
    return jsonify({"success": True})

  return render_template("payment_report.jinja2",**data)


@app.route("/member_report")
@login_required
def member_payment_report():
  increment = float(request.args.get("increment", 0.0))
  end = datetime.now().date()
  start = end - timedelta(days=7)

  day   = int(request.args.get("from_day", start.day))
  month = int(request.args.get("from_month", start.month))
  year  = int(request.args.get("from_year", start.year))
  from_date = datetime(year, month, day).date()

  day   = int(request.args.get("to_day", end.day))
  month = int(request.args.get("to_month", end.month))
  year  = int(request.args.get("to_year", end.year))
  to_date = datetime(year, month, day).date()

  if to_date > end:
    to_date = end
    flash(str(lazy_gettext("To Date cannot be greater than today!")), "error")

  if to_date < from_date:
    to_date = end
    from_date = start
    flash(str(lazy_gettext("From Date cannot be greater than to date!")), "error")

  from_member = int(request.args.get("from_member", 1))
  to_member = int(request.args.get("to_member", 10))

  member_service = MemberService()
  mlst = member_service.search()
  member_list = {}
  for x in mlst:
    member_list[x.id] = x

  if from_member not in member_list or to_member not in member_list:
    flash(gettext("Invalid member code range"), "error")
    from_member = 1
    to_member = 10

  lst, summary = get_collection_search_data(from_member, from_date, to_date, increment)
  data = dict(from_date=from_date,
    to_date=to_date,lst=lst,
    from_member=from_member,to_member=to_member,
    increment=increment,summary=summary,member_list=member_list)

  if request.args.get("print", "False") == "True":
    for x in range(from_member, to_member+1):
      if x not in member_list:
        continue
      lst, summary = get_collection_search_data(x, from_date, to_date, increment)
      #if not lst or len(lst) == 0:
      #  continue
      print_data = dict(from_date=from_date,
                        to_date=to_date,lst=lst,
                        from_member=from_member,to_member=to_member,
                        increment=increment,summary=summary,member_list=member_list)
      do_print_report("member_report.jinja2", "member_report_%d.pdf" % (x), **print_data)
    return jsonify({"success": True})

  return render_template("member_report.jinja2",**data)


def get_collection_search_data(member_id, from_date, to_date, increment):
  collectionService = MilkCollectionService()
  lst = collectionService.search_by_date(member_id=member_id,from_date=from_date,to_date=to_date)
  summary = {"qty": 0.0, "fat": 0.0,  "snf": 0.0, "rate": 0, "amount": 0, "increment": 0, "total": 0}


  summary["qty"] = sum([x.qty for x in lst])
  if summary["qty"] > 0.0:
    summary["fat"] = sum([x.fat * x.qty for x in lst])/summary["qty"]
    summary["snf"] = sum([x.snf * x.qty for x in lst])/summary["qty"]
    summary["rate"] = sum([x.rate * x.qty for x in lst])/summary["qty"]

  summary["amount"] = sum([x.total for x in lst])
  summary["increment"] = summary["qty"] * increment
  summary["total"] = summary["increment"] + summary["amount"]

  return lst, summary


@app.route("/dairy_report")
@login_required
def dairy_report():
  end = datetime.now().date()
  start = end - timedelta(days=7)

  day   = int(request.args.get("from_day", start.day))
  month = int(request.args.get("from_month", start.month))
  year  = int(request.args.get("from_year", start.year))
  from_date = datetime(year, month, day).date()

  day   = int(request.args.get("to_day", end.day))
  month = int(request.args.get("to_month", end.month))
  year  = int(request.args.get("to_year", end.year))
  to_date = datetime(year, month, day).date()

  if to_date > end:
    to_date = end
    flash(str(lazy_gettext("To Date cannot be greater than today!")), "error")

  if to_date < from_date:
    to_date = end
    from_date = start
    flash(str(lazy_gettext("From Date cannot be greater than to date!")), "error")

  collectionService = MilkCollectionService()
  col_lst = collectionService.search_by_date(member_id=None,from_date=from_date,to_date=to_date)
  lst = {}

  for x in col_lst:
    d = x.created_at.date()
    if not d in lst.keys():
      lst[d] = {}
      lst[d][x.shift] = { "qty": x.qty, "rate": (x.rate * x.qty),
                          "fat": x.fat * x.qty, "snf": x.snf * x.qty,
                          "total": x.total }
    else:
      if not x.shift in lst[d]:
        lst[d][x.shift] = { "qty": x.qty, "rate": (x.rate * x.qty),
                          "fat": x.fat * x.qty, "snf": x.snf * x.qty,
                          "total": x.total }
      else:
        item = lst[d][x.shift]
        item["qty"]  = item["qty"] + x.qty
        item["rate"] = (item["rate"] + (x.rate * x.qty))
        item["fat"]  = (item["fat"] + (x.fat * x.qty))
        item["snf"]  = (item["snf"] + (x.snf * x.qty))
        item["total"]= item["total"] + x.total

  summary = {"fat": 0.0, "snf": 0.0, "qty": 0.0, "rate": 0, "total": 0}
  kg_fat = 0
  kg_snf = 0
  kg_rate = 0
  for d in lst.keys():
    for shift in lst[d].keys():
      item = lst[d][shift]
      item["fat"] = item["fat"]/item["qty"]
      item["snf"] = item["snf"]/item["qty"]
      item["rate"] = item["rate"]/item["qty"]

      kg_fat = kg_fat + item["fat"]
      kg_snf = kg_snf + item["snf"]
      kg_rate= kg_rate + item["rate"]
      summary["qty"] = summary["qty"] + item["qty"]
      summary["total"] = summary["total"] + item["total"]

  summary["fat"] = kg_fat/len(lst)
  summary["snf"] = kg_snf/len(lst)
  summary["rate"] = kg_rate/len(lst)

  data = dict(from_date=from_date,to_date=to_date,lst=lst,summary=summary)

  if request.args.get("print", "False") == "True":
    do_print_report("dairy_report.jinja2", "dairy_report.pdf", **data)
    return jsonify({"success": True})

  return render_template("dairy_report.jinja2", **data)


@app.route("/settings_report")
@login_required
def settings_report():
  settings = g.app_settings
  basic_keys = ["SOCIETY_NAME","SOCIETY_ADDRESS","SOCIETY_ADDRESS1","HEADER_LINE1","HEADER_LINE2","HEADER_LINE3","HEADER_LINE4", "FOOTER_LINE1", "FOOTER_LINE2"]
  settings_keys = ["ANALYZER_TYPE","SCALE_TYPE","RATE_TYPE","COLLECTION_PRINTER_TYPE",
  "MANUAL_FAT", "MANUAL_SNF", "MANUAL_QTY","PRINT_BILL","PRINT_CLR","PRINT_WATER", 
  "BILL_OVERWRITE", "QUANTITY_2_DECIMAL","LANGUAGE","DATA_EXPORT_FORMAT", "SEND_SMS", 
  "CAN_CAPACITY", "ANALYZER_PORT", "WEIGH_SCALE_PORT", "GSM_PORT", "THERMAL_PRINTER_PORT"]

  data = dict(settings=settings, basic_keys=basic_keys,settings_keys=settings_keys)

  if request.args.get("print", "False") == "True":
    do_print_report("settings_report.jinja2", "settings_report.pdf", **data)
    return jsonify({"success": True})

  return render_template("settings_report.jinja2", **data)