from flask import render_template, request, redirect, g, flash, jsonify, session
from flask_login import login_required, current_user
from datetime import datetime
from dateutil import parser
import json
import os

from web import app, fmtDecimal, format_currency, get_currency_symbol, send_to_thermal_printer, settings_provider

from flask_babel import lazy_gettext
from services.member_service import MemberService
from services.milkcollection_service import MilkCollectionService
from services.rate_service import RateService
from services.rate_calc import RateCalc

from configuration_manager import ConfigurationManager

from models import *
from hal import *

def get_current_can_count():
  return session.get("can_count", 1)

def sendSms(entity, address):
  mobile = entity.member.mobile
  #mobile = "+919789443696"
  #mobile = "+919952463624"

  tmp = app.jinja_env.get_template("thermal/ticket_sms.jinja2")
  data = settings_provider()
  data.update(entity=entity)
  markup = tmp.render(data)

  modem = SmsService(address=address)
  modem.send(mobile, markup)


@app.route("/collection", methods=['GET', 'POST'])
@login_required
def collection():
  shift = "MORNING"
  date = datetime.now()
  settings = g.app_settings

  changeDate = request.args.get("btnChangeDate", "False") == "True"

  if changeDate:
    day, month, year  = request.args.get("day", date.day), request.args.get("month", date.month), request.args.get("year", date.year)
    shift = request.args.get("shift", shift)
    time = "09:00 AM"
    if shift == "EVENING":
      time = "03:01 PM"
    created_at = "%s/%s/%s %s" % (day,month,year,time)
    date1 = parser.parse(created_at, default=date, dayfirst=True)

    if date1 > date:
      flash(str(lazy_gettext("Date cannot be greater than today!")), "error")
    else:
      date = date1

  if date.hour >= 15:
    shift = "EVENING"

  member_service = MemberService()
  collectionService = MilkCollectionService()

  if request.method == "POST":
    entity = {}
    member_code = request.form.get("member_code")
    if member_code and len(member_code) > 0 and member_code.isdigit():
      mcode = int(member_code)
      collection_id = request.form.get("collection_id", None)
      entity["member"] = member_service.get(mcode)
      entity["shift"] = request.form.get("shift", shift)
      entity["fat"] = float(request.form.get("fat"))
      entity["snf"] = float(request.form.get("snf"))
      entity["clr"] = float(request.form.get("clr"))
      entity["aw"] = float(request.form.get("water"))
      entity["qty"] = float(request.form.get("qty"))
      entity["rate"] = float(request.form.get("rate"))
      entity["total"] = float(request.form.get("total"))
      entity["created_by"] = current_user.id
      entity["created_at"] = parser.parse(request.form.get("created_at", str(date)))
      entity["status"] = True
      entity["can_no"] = get_current_can_count()

      if collection_id and int(collection_id) > 0:
        collectionService.update(int(collection_id), entity)
      else:
        collection_id = collectionService.add(entity)

      can_print_bill = bool(settings[SystemSettings.PRINT_BILL])
      can_send_sms =  bool(settings[SystemSettings.SEND_SMS])

      saved_entity = collectionService.get(collection_id)
      if can_print_bill:
        try:
          printTicket(saved_entity)
        except Exception as e:
          print "print exception:", e
          flash(str(lazy_gettext("Error in printing!")), "error")

      if can_send_sms:
        sendSms(saved_entity, settings[SystemSettings.GSM_PORT])

      do_tare_scale(settings)

      flash("Saved successfully!", "success")
    else:
      flash("Invalid data!", "error")
    return redirect("/collection")

  member_list = member_service.search()
  members_json = json.dumps([{'id': x.id, 'name': x.name, 'cattle_type': x.cattle_type} for x in member_list])

  collection_members, mcollection, summary = collectionService.get_milk_collection_and_summary(shift, date.date())

  can_capacity = float(settings[SystemSettings.CAN_CAPACITY])
  current_can_no = get_current_can_count()
  if current_can_no == 1:
    current_can_no = collectionService.get_latest_can(shift, date.date())
    session["can_count"] = current_can_no

  can_litres = collectionService.get_total_litres(shift=shift, can_no=current_can_no, created_at=date.date())
  can_height = (1 - ((can_capacity - can_litres)/can_capacity))*100.0

  currency_symbol = get_currency_symbol()

  return render_template('collection.jinja2',
    shift=shift,
    member_list=member_list,
    members_json=members_json,
    date=date,
    summary=summary,
    can_litres=can_litres,
    can_height=can_height,
    currency_symbol=currency_symbol,
    current_can_no=current_can_no)


@app.route("/get_collection_data")
@login_required
def get_collection_data():
  member_id = request.args.get("member_id", None)
  shift = request.args.get("shift", None)
  cattle_type = request.args.get("cattle_type", "COW")
  today = datetime.now()
  created_at = parser.parse(request.args.get("created_at", str(today))).date()
  data = { "collection_id": None, "currency_symbol": get_currency_symbol() }
  collectionService = MilkCollectionService()

  if member_id and int(member_id) > 0 and shift and created_at:
    lst = collectionService.search(member_id=int(member_id), shift=shift, created_at=created_at)
    if lst and len(lst) > 0:
      entity = lst[0]
      data["collection_id"] = entity.id
      data["shift"] = entity.shift
      data["member_id"] = entity.member.id
      data["cattle_type"] = entity.member.cattle_type
      data["created_at"] = entity.created_at
      data["fat"] = entity.fat
      data["snf"] = entity.snf
      data["clr"] = entity.clr
      data["water"] = entity.aw
      data["qty"] = entity.qty
      data["rate"] = entity.rate
      data["total"] = entity.total
      data["fmt_rate"] = format_currency(entity.rate)
      data["fmt_total"] = format_currency(entity.total)
      data["can_litres"] = None
      data["can_height"] = None
      override = request.args.get("override", "False")
      if override == "False":
        return jsonify(**data)

  rateCalc = RateCalc(g.app_settings[SystemSettings.RATE_TYPE])

  sensor_data = get_sensor_data()

  fat = data["fat"] = fmtDecimal(sensor_data["fat"])
  snf = data["snf"] = fmtDecimal(sensor_data["snf"])
  data["clr"] = fmtDecimal(sensor_data["clr"])
  data["water"] = fmtDecimal(sensor_data["water"])

  qty = data["qty"] = fmtDecimal(sensor_data["qty"])

  rate = fmtDecimal(rateCalc.get_rate(cattle_type, fat, snf))
  total = fmtDecimal(rate * qty)

  data["rate"] = rate
  data["total"] = total
  data["fmt_rate"] = format_currency(rate)
  data["fmt_total"] = format_currency(total)

  can_capacity = float(g.app_settings[SystemSettings.CAN_CAPACITY])
  current_can_no = get_current_can_count()

  if current_can_no == 1:
    current_can_no = collectionService.get_latest_can(shift, created_at)
    session["can_count"] = current_can_no

  can_litres = qty + collectionService.get_total_litres(shift=shift, can_no=current_can_no, created_at=created_at)
  can_height = (1 - ((can_capacity - can_litres)/can_capacity))*100.0

  data["can_litres"] = can_litres
  data["can_height"] = can_height

  return jsonify(**data)


@app.route("/get_qty_data")
@login_required
def get_qty_data():
  member_id = request.args.get("member_id", None)
  shift = request.args.get("shift", None)
  cattle_type = request.args.get("cattle_type", "COW")
  today = datetime.now()
  created_at = parser.parse(request.args.get("created_at", str(today))).date()
  collectionService = MilkCollectionService()

  if member_id and int(member_id) > 0 and shift and created_at:
    lst = collectionService.search(member_id=int(member_id), shift=shift, created_at=created_at)
    if lst and len(lst) > 0:
      return jsonify({"status" : "failure"})

  settings = g.app_settings
  scale = WeightScale(settings[SystemSettings.SCALE_TYPE], address=settings[SystemSettings.WEIGH_SCALE_PORT], qty2decimal=settings[SystemSettings.QUANTITY_2_DECIMAL])
  qty = scale.get()

  can_capacity = float(g.app_settings[SystemSettings.CAN_CAPACITY])
  current_can_no = get_current_can_count()

  can_litres = qty + collectionService.get_total_litres(shift=shift, can_no=current_can_no, created_at=created_at)
  can_height = (1 - ((can_capacity - can_litres)/can_capacity))*100.0

  return jsonify({"status" : "success", "value": qty, "can_litres": can_litres, "can_height": can_height})


@app.route("/get_manual_data")
@login_required
def get_manual_data():
  cattle_type = request.args.get("cattle_type", "COW")
  rateCalc = RateCalc(g.app_settings[SystemSettings.RATE_TYPE])

  fat = float(request.args.get("fat", 0.0))
  snf = float(request.args.get("snf", 0.0))
  qty = float(request.args.get("qty", 0.0))
  clr = 4.0* ((snf - (0.21 * fat)) - 0.36)
  S = 8.5
  if cattle_type != "COW":
    S = 9.0
  aw = (((S-snf)/S)*100.0) - 0.7

  if aw < 0.0:
    aw = 0.0

  rate = fmtDecimal(rateCalc.get_rate(cattle_type, fat, snf))
  total = fmtDecimal(rate * qty)

  data = { "status" : "success", "currency_symbol": get_currency_symbol() }
  data["clr"] = fmtDecimal(clr)
  data["water"] = fmtDecimal(aw)
  data["rate"] = rate
  data["total"] = total
  data["fmt_rate"] = format_currency(rate)
  data["fmt_total"] = format_currency(total)
  return jsonify(data)


def get_sensor_data():
  settings = g.app_settings
  scale = WeightScale(settings[SystemSettings.SCALE_TYPE], address=settings[SystemSettings.WEIGH_SCALE_PORT], qty2decimal=settings[SystemSettings.QUANTITY_2_DECIMAL])
  analyzer = MilkAnalyzer(settings[SystemSettings.ANALYZER_TYPE], address=settings[SystemSettings.ANALYZER_PORT])
  data = analyzer.get()
  data["qty"] = scale.get()
  return data

def do_tare_scale(settings):
  scale = WeightScale(settings[SystemSettings.SCALE_TYPE], address=settings[SystemSettings.WEIGH_SCALE_PORT], qty2decimal=settings[SystemSettings.QUANTITY_2_DECIMAL])
  success = scale.tare()
  print "Tare scale: %s" % (success)
  return success

@app.route("/tare_scale")
@login_required
def tare_scale():
  success = do_tare_scale(g.app_settings)
  return jsonify(success=success)


@app.route("/tare_can")
@login_required
def tare_can():
  session["can_count"] = get_current_can_count() + 1
  print "Tare can: ", session["can_count"]
  return jsonify(success=True)


def printTicket(entity):
  tmp = app.jinja_env.get_template("thermal/ticket.jinja2")
  data = settings_provider()
  data.update(entity=entity)
  markup = tmp.render(data)
  send_to_thermal_printer(markup)
