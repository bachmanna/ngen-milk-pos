from flask import Flask, session, render_template, request, redirect, g, flash, jsonify
from flask_login import login_required, login_user, logout_user, current_user, LoginManager
from passlib.handlers.md5_crypt import md5_crypt
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from dateutil import parser
from flask.ext.babel import Babel
import json
import random


app = Flask(__name__, instance_relative_config=False)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
db.create_all()

# localization
babel = Babel(app)


from services.user_service import UserService
from services.member_service import MemberService
from services.milkcollection_service import MilkCollectionService
from services.rate_service import RateService
from models import *


def fmtDecimal(value):
  if isinstance(value, float):
    return float("{0:.2f}".format(value))
  return value


class FATRateCalculator(object):
  def get_rate(self, cattle_type, fat, snf):
    rate_service = RateService()
    rate_list = rate_service.get_fat_collection_rate(cattle_type)
    if not rate_list or len(rate_list) == 0:
      return 0.0
    for x in rate_list:
      if fat >= x.min_value and fat <= x.max_value:
        return x.rate/10.0
    return 0.0

class FATSNFRateCalculator(object):
  def get_rate(self, cattle_type, fat, snf):
    return 0

class TS1RateCalculator(object):
  def get_rate(self, cattle_type, fat, snf):
    return 0

class TS2RateCalculator(object):
  def get_rate(self, cattle_type, fat, snf):
    rate_service = RateService()
    ts1 = fmtDecimal(fat + snf)
    rate_list = rate_service.get_ts2_collection_rate(cattle_type)
    if not rate_list or len(rate_list) == 0:
      return 0
    for x in rate_list:
      if ts1 >= x.min_value and ts1 <= x.max_value:
        return x.rate/10.0
    return 0.0

#Rate calculator setup
rate_calculator = {
                    CollectionRateType.FAT: FATRateCalculator(),
                    CollectionRateType.FAT_AND_SNF: FATSNFRateCalculator(),
                    CollectionRateType.TS_1: TS1RateCalculator(),
                    CollectionRateType.TS_2: TS2RateCalculator(),
                  }

def testdata():
  db.drop_all()
  db.create_all()
  from test_data import TestData
  test = TestData()
  test.create_members()
  test.test_settings()
  test.test_rate_setup()
  test.create_default_users()
  #test.datetime_test()
  db.session.commit()

#testdata()

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"
login_manager.login_message = None

from models.User import User
from configuration_manager import ConfigurationManager

@babel.localeselector
def get_locale():
  return g.get('current_lang', 'ta')

@login_manager.user_loader
def get_user(id):
  service = UserService()
  user = service.get(_id=id)
  if user:
    return User(user_id=id, name=user.name, email=user.email, roles=user.roles.split(","))
  return None


@app.before_request
def set_user_on_request_g():
  config_manager = ConfigurationManager()
  settings = config_manager.get_all_settings()
  setattr(g, 'user', current_user)
  setattr(g, 'app_settings', settings)
  setattr(g, 'current_lang', settings.get("LANGUAGE", "ta"))


@app.context_processor
def settings_provider():
    settings = g.app_settings

    d = datetime.now().strftime("%d/%m/%Y")
    t = datetime.now().strftime("%I:%M%p")

    return dict(settings=settings, date=d, time=t)


@app.route("/")
@login_required
def home():
  return render_template('home.jinja2')


@app.route("/collection", methods=['GET', 'POST'])
@login_required
def collection():
  shift = "MORNING"
  date = datetime.now()
  if date.hour >= 15:
    shift = "EVENING"

  member_service = MemberService()

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
    collectionService = MilkCollectionService()
    if collection_id and int(collection_id) > 0:
      collectionService.update(int(collection_id), entity)
      print "update", collection_id, 
    else:
      collectionService.add(entity)
      print "add"

    flash("Saved successfully!")
    return redirect("/collection")
  
  member_list = member_service.search()
  members_json = json.dumps([{'id': x.id, 'name': x.name, 'cattle_type': x.cattle_type} for x in member_list])

  collection_members, mcollection, summary = get_milk_collection_and_summary(shift, date.date())

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
  rateCalc = rate_calculator[g.app_settings[SystemSettings.RATE_TYPE]]
  fat = data["fat"] = fmtDecimal(random.random()*10.0)
  snf = data["snf"] = fmtDecimal(random.random()*20.0)
  data["clr"] = fmtDecimal(random.random()*15.0)
  data["water"] = fmtDecimal(random.random()*80.0)
  qty = data["qty"] = fmtDecimal(random.random()*12.0)
  rate = data["rate"] = fmtDecimal(rateCalc.get_rate(cattle_type, fat, snf))
  data["total"] = fmtDecimal(rate * qty)
  return jsonify(**data)

@app.route("/basic_setup", methods=['GET', 'POST'])
@login_required
def basic_setup():
  if request.method == 'POST':
    settings = {}
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


@app.route("/system_setup")
@login_required
def system_setup():
  return render_template("system_setup.jinja2")


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
    min_value = float(request.form.get("min_value", 0.0))
    max_value = float(request.form.get("max_value", 0.0))
    rate = float(request.form.get("rate", 0.0))
    cattle_type = request.form.get("cattle_type", "COW")
    rate_service.update_fat_collection_rate(cattle_type,id,min_value,max_value,rate)

  rate_list = rate_service.get_fat_collection_rate(cattle_type=cattle_type)
  return render_template("rate_fat.jinja2", cattle_type=cattle_type, rate_list=rate_list)


@app.route("/member", methods=['GET', 'POST'])
@login_required
def manager_member():
  member_service = MemberService()
  if request.method == 'POST':
    code = request.form.get("code")
    name = request.form.get("name")
    mobile = request.form.get("mobile")
    cattle_type = request.form.get("cattle_type")
    if code and name and int(code):
      id = int(code)
      m = member_service.get(id)
      if not m:
        member_service.add(name, cattle_type, mobile, _id=id)
      else:
        member_service.update(id, name, cattle_type, mobile)
    else:
      flash("Invalid member data.")
  member_list = member_service.search()
  free_list = []
  used_list = [int(x.id) for x in member_list]
  for i in range(1,100):
    if len(free_list) > 10:
        break
    if i not in used_list:
      free_list.append(str(i))

  return render_template("member.jinja2",member_list=member_list, free_list=free_list)


@app.route("/data_reset")
@login_required
def data_reset():
  return render_template("data_reset.jinja2")


@app.route("/user", methods=['GET', 'POST'])
@login_required
def manage_user():
  service = UserService()
  user = User(user_id="",name="")
  if request.method == 'POST':
    id = request.form["id"]
    name = request.form["name"]
    password = request.form["password"]
    if id and int(id) and name:
      if password and len(password) > 4:
        password = md5_crypt.encrypt(password)
        if service.update(id, name, password):
          flash("User update successfully!")
      else:
        flash("Password should be greater than 4 letters!")
    else:
      flash("Invalid user id.")

  user_list = service.search()
  return render_template("manage_user.jinja2", user=user, user_list=user_list)


@app.route("/factory_reset")
@login_required
def factory_reset():
  testdata()
  return render_template("factory_reset.jinja2")


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

  members, mcollection, summary = get_milk_collection_and_summary(shift, search_date)

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

  members, mcollection, summary = get_milk_collection_and_summary(shift, search_date)
  return render_template("shift_summary.jinja2", mcollection=mcollection, member_list=members, summary=summary, search_date=search_date, shift=shift)


def get_milk_collection_and_summary(shift, search_date):
  member_service = MemberService()
  member_list = member_service.search()  
  members = {}
  for x in member_list:
    members[x.id] = x
  collectionService = MilkCollectionService()
  mcollection = collectionService.search(None, shift=shift, created_at=search_date)
  cow_collection = [x for x in mcollection if members[x.member.id].cattle_type == "COW"]
  buffalo_collection = [x for x in mcollection if members[x.member.id].cattle_type == "BUFFALO"]
  summary = {}
  summary["member"] = [len(cow_collection),  len(buffalo_collection)]
  summary["milk"] = [sum([x.qty for x in cow_collection]), sum([x.qty for x in buffalo_collection])]
  summary["fat"] = [0,0]
  summary["snf"] = [0,0]
  summary["rate"] = [0,0]

  if summary["milk"][0] != 0:
    summary["fat"][0] = sum([x.fat for x in cow_collection])/summary["milk"][0]
    summary["snf"][0] = sum([x.snf for x in cow_collection])/summary["milk"][0]
    summary["rate"][0] = sum([x.rate for x in cow_collection])/summary["milk"][0]

  if summary["milk"][1] != 0:
    summary["fat"][1] = sum([x.fat for x in buffalo_collection])/summary["milk"][1]
    summary["snf"][1] = sum([x.snf for x in buffalo_collection])/summary["milk"][1]
    summary["rate"][1] = sum([x.rate for x in buffalo_collection])/summary["milk"][1]  
  
  summary["total"] = [sum([x.total for x in cow_collection]), sum([x.total for x in buffalo_collection])]
  return members, mcollection, summary

@app.route("/login", methods=['GET', 'POST'])
def login():
  service = UserService()
  username = service.get(1).name
  if request.method == 'POST':
      username = request.form["username"]
      password = request.form["password"]
      if username and password and len(password) > 4:
        service = UserService()
        users = service.search(name=username)
        if users and len(users) == 1 and md5_crypt.verify(password, users[0].password):
          dbuser = users[0]
          user = User(user_id=dbuser.id, name=dbuser.name, email=dbuser.email, roles=dbuser.roles.split(","))
          login_user(user, remember=False)
          return redirect("/")
      flash("Invalid username or password!")
  return render_template('login.jinja2', username=username)


@app.route('/logout')
@app.route('/logout/')
def app_logout():
  logout_user()
  session.clear()
  return redirect('/')