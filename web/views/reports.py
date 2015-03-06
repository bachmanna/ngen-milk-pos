from flask import render_template, request, redirect, g, flash
from flask_login import login_required
from datetime import datetime

from web import app

from services.member_service import MemberService
from services.rate_service import RateService
from services.milkcollection_service import MilkCollectionService
from models import *

@app.route("/reports")
@login_required
def reports():
  return render_template("reports.jinja2")


@app.route("/member_list")
@login_required
def report_member_list():
  member_service = MemberService()
  member_list = member_service.search()
  return render_template("member_list.jinja2",member_list=member_list)

@app.route("/detail_shift")
@login_required
def report_detail_shift():
  shift = request.args.get("shift", "MORNING")
  today = datetime.now().date()
  day   = int(request.args.get("day", today.day))
  month = int(request.args.get("month", today.month))
  year  = int(request.args.get("year", today.year))
  search_date = datetime(year, month, day).date()
  collectionService = MilkCollectionService()
  members, mcollection, summary = collectionService.get_milk_collection_and_summary(shift, search_date)

  return render_template("detail_shift.jinja2", mcollection=mcollection, member_list=members, summary=summary, search_date=search_date, shift=shift)

@app.route("/shift_summary")
@login_required
def report_shift_summary():
  shift = request.args.get("shift", "MORNING")
  today = datetime.now().date()
  day   = int(request.args.get("day", today.day))
  month = int(request.args.get("month", today.month))
  year  = int(request.args.get("year", today.year))
  search_date = datetime(year, month, day).date()
  collectionService = MilkCollectionService()
  members, mcollection, summary = collectionService.get_milk_collection_and_summary(shift, search_date)
  return render_template("shift_summary.jinja2", mcollection=mcollection, member_list=members, summary=summary, search_date=search_date, shift=shift)
