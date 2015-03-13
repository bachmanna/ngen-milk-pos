from flask import render_template, request, redirect, g, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from dateutil import parser
import json
import random

from web import app, fmtDecimal

from flask.ext.babel import lazy_gettext
from services.member_service import MemberService
from services.milkcollection_service import MilkCollectionService
from services.rate_service import RateService
from services.rate_calc import RateCalc

from models import *

@app.route("/collection", methods=['GET', 'POST'])
@login_required
def collection():
  shift = "MORNING"
  date = datetime.now()

  changeDate = request.args.get("btnChangeDate", "False") == "True"

  if changeDate:
    day, month, year  = request.args.get("day", date.day), request.args.get("month", date.month), request.args.get("year", date.year)
    hour, minute, dn = request.args.get("hour", date.hour), request.args.get("minute", date.minute), request.args.get("dn", date.strftime("%p"))
    created_at = "%s/%s/%s %s:%s%s" % (day,month,year,hour,minute,dn)
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
    mcode = int(request.form.get("member_code"))
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
    print entity
    if collection_id and int(collection_id) > 0:
      collectionService.update(int(collection_id), entity)
    else:
      collectionService.add(entity)

    flash("Saved successfully!", "success")
    return redirect("/collection")
  
  member_list = member_service.search()
  members_json = json.dumps([{'id': x.id, 'name': x.name, 'cattle_type': x.cattle_type} for x in member_list])

  collection_members, mcollection, summary = collectionService.get_milk_collection_and_summary(shift, date.date())

  return render_template('collection.jinja2',
    shift=shift,
    member_list=member_list,
    members_json=members_json,
    date=date,
    collection_members=collection_members,
    summary=summary)


@app.route("/get_collection_data")
@login_required
def get_collection_data():
  member_id = request.args.get("member_id", None)
  shift = request.args.get("shift", None)
  cattle_type = request.args.get("cattle_type", "COW")
  today = datetime.now()
  created_at = parser.parse(request.form.get("created_at", str(today))).date()
  data = { "collection_id": None }

  if member_id and shift and created_at:
    collectionService = MilkCollectionService()
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
      return jsonify(**data)

  rateCalc = RateCalc(g.app_settings[SystemSettings.RATE_TYPE])
  
  fat = data["fat"] = fmtDecimal(random.random()*10.0)
  snf = data["snf"] = fmtDecimal(random.random()*20.0)
  data["clr"] = fmtDecimal(random.random()*15.0)
  data["water"] = fmtDecimal(random.random()*80.0)
  qty = data["qty"] = fmtDecimal(random.random()*12.0)
  rate = data["rate"] = fmtDecimal(rateCalc.get_rate(cattle_type, fat, snf))
  data["total"] = fmtDecimal(rate * qty)
  return jsonify(**data)