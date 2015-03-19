from flask import render_template, request, redirect, g, flash, url_for, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from flask.ext.babel import lazy_gettext, gettext

from web import app, settings_provider

from services.member_service import MemberService
from services.rate_service import RateService
from services.milkcollection_service import MilkCollectionService
from models import *

import os
import sys
#import xhtml2pdf.pisa as pisa

from flask_weasyprint import HTML, CSS

styles = None

def do_print_report(template,outfile, **kwargs):
  global styles
  bakdir = os.path.join(app.root_path, 'backup')
  if not os.path.exists(bakdir):
      os.makedirs(bakdir)

  dest = os.path.join(bakdir, outfile)
  tmp = app.jinja_env.get_template(template)
  s = settings_provider() or {}
  s.update(**kwargs)
  data = tmp.render(s)

  if styles is None:
    app_css = CSS(url_for("static", filename="css/app.css"))
    custom_css = CSS(url_for("static", filename="css/custom.css"))
    print_css = CSS(url_for("static", filename="css/print.css"))
    styles = [app_css,custom_css,print_css]
  HTML(string=data).write_pdf(target=dest, stylesheets = styles)
  if sys.platform == "win32":
    import xhtml2pdf.pisa as pisa
    pisa.startViewer(dest)

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
    do_print_report("reports/member_list.jinja2", "member_list.pdf", **data)
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
    do_print_report("reports/absence_list.jinja2", "absence_list.pdf", **data)
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
    do_print_report("reports/detail_shift.jinja2", "detail_shift.pdf", **data)
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
    do_print_report("reports/shift_summary.jinja2", "shift_summary.pdf", **data)
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

  for x in col_lst:
    if not x.member_id in lst.keys():
      inc = x.qty * increment
      total = x.total + inc
      lst[x.member_id] = { "qty": x.qty, "rate": x.rate, 
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
    summary["rate"] = summary["rate"] + item["rate"]
    summary["amount"] = summary["amount"] + item["amount"]
    summary["increment"] = summary["increment"] + item["increment"]
    summary["total"] = summary["total"] + item["total"]

  data = dict(from_date=from_date,to_date=to_date,lst=lst,increment=increment,summary=summary)

  if request.args.get("print", "False") == "True":
    do_print_report("reports/payment_report.jinja2", "payment_report.pdf", **data)
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

  from_member = float(request.args.get("from_member", 1))
  to_member = float(request.args.get("to_member", 100))

  collectionService = MilkCollectionService()
  lst = collectionService.search_by_date(member_id=from_member,from_date=from_date,to_date=to_date)
  summary = {"qty": 0.0, "rate": 0, "amount": 0, "increment": 0, "total": 0}

  summary["qty"] = sum([x.qty for x in lst])
  summary["rate"] = sum([x.rate for x in lst])
  summary["amount"] = sum([x.total for x in lst])
  summary["increment"] = summary["qty"] * increment
  summary["total"] = summary["increment"] + summary["amount"]

  member_service = MemberService()
  mlst = member_service.search()
  member_list = {}
  for x in mlst:
    member_list[x.id] = x

  data = dict(from_date=from_date,
    to_date=to_date,lst=lst,
    from_member=from_member,to_member=to_member,
    increment=increment,summary=summary,member_list=member_list)

  if request.args.get("print", "False") == "True":
    do_print_report("reports/member_report.jinja2", "member_report.pdf", **data)
    return jsonify({"success": True})

  return render_template("member_report.jinja2",**data)


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
      lst[d][x.shift] = { "qty": x.qty, "rate": x.rate,
                          "fat": x.fat, "snf": x.snf,
                          "total": x.total }
    else:
      if not x.shift in lst[d]:
        lst[d][x.shift] = { "qty": x.qty, "rate": x.rate,
                          "fat": x.fat, "snf": x.snf,
                          "total": x.total }
      else:
        item = lst[d][x.shift]
        item["qty"] = item["qty"] + x.qty
        item["rate"] = item["rate"] + x.rate
        item["fat"] = item["fat"] + x.fat
        item["snf"] = item["snf"] + x.snf
        item["total"] = item["total"] + x.total

  summary = {"qty": 0.0, "rate": 0, "total": 0}
  for d in lst.keys():
    for shift in lst[d].keys():
      item = lst[d][shift]
      summary["qty"] = summary["qty"] + item["qty"]
      summary["rate"] = summary["rate"] + item["rate"]
      summary["total"] = summary["total"] + item["total"]

  data = dict(from_date=from_date,to_date=to_date,lst=lst,summary=summary)

  if request.args.get("print", "False") == "True":
    do_print_report("reports/dairy_report.jinja2", "dairy_report.pdf", **data)
    return jsonify({"success": True})

  return render_template("dairy_report.jinja2", **data)


@app.route("/settings_report")
@login_required
def settings_report():
  settings = g.app_settings
  basic_keys = ["SOCIETY_NAME","SOCIETY_ADDRESS","SOCIETY_ADDRESS1","HEADER_LINE1","HEADER_LINE2","HEADER_LINE3","HEADER_LINE4", "FOOTER_LINE1", "FOOTER_LINE2"]
  settings_keys = ["ANALYZER_TYPE","SCALE_TYPE","RATE_TYPE","COLLECTION_PRINTER_TYPE","MANUAL_FAT", "MANUAL_SNF", "MANUAL_QTY","PRINT_BILL","PRINT_CLR","PRINT_WATER", "BILL_OVERWRITE", "QUANTITY_2_DECIMAL","LANGUAGE","DATA_EXPORT_FORMAT"]

  data = dict(settings=settings, basic_keys=basic_keys,settings_keys=settings_keys)

  if request.args.get("print", "False") == "True":
    do_print_report("reports/settings_report.jinja2", "settings_report.pdf", **data)
    return jsonify({"success": True})

  return render_template("settings_report.jinja2", **data)