from flask import Flask, session, render_template, request, redirect, g, flash
from flask_login import login_required, login_user, logout_user, current_user, LoginManager
from passlib.handlers.md5_crypt import md5_crypt
from pony.orm import sql_debug, db_session
from datetime import datetime

from services.user_service import UserService
from services.member_service import MemberService

app = Flask(__name__, instance_relative_config=False)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

from models import *

sql_debug(False)
db.generate_mapping(create_tables=True)


def create_default_users():
  user_service = UserService()
  created_by = 4
  if current_user:
    created_by = current_user.id
  user_service.add("basic", "$1$yWq10SD.$WQlvdj6kmHOY9KjHhuIGn1", "basic@milkpos.in", ["basic"], created_by)
  user_service.add("setup", "$1$Ii9Edtkd$cpxJMzTgpCmFxEhka2nKs/", "setup@milkpos.in", ["setup"], created_by)
  user_service.add("support", "$1$P/A0YAOn$O8SuzMiowBVJAorhfY239/", "support@milkpos.in", ["support"], created_by)
  user_service.add("admin", "$1$doG2/gED$vTLr/Iob7T9z0.nydnJxD1", "admin@milkpos.in", ["admin"], created_by)


def testdata():
  db.drop_all_tables(with_all_data=True)
  db.create_tables()
  with db_session:
      from test_data import TestData
      test = TestData()
      test.create_members()
      test.test_settings()
      create_default_users()
      #test.datetime_test()

#testdata()

app.wsgi_app = db_session(app.wsgi_app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"
login_manager.login_message = None

from models.User import User
from configuration_manager import ConfigurationManager

@login_manager.user_loader
def get_user(id):
  service = UserService()
  user = service.get(_id=id)
  if user:
    return User(user_id=id, name=user.name, email=user.email, roles=user.roles.split(","))
  return None


@app.before_request
def set_user_on_request_g():
  setattr(g, 'user', current_user)


@app.context_processor
def settings_provider():
    config_manager = ConfigurationManager()
    settings = config_manager.get_all_settings()

    d = datetime.now().strftime("%d/%m/%Y")
    t = datetime.now().strftime("%I:%M%p")

    return dict(settings=settings, date=d, time=t)


@app.route("/")
@login_required
def home():
  return render_template('home.jinja2')


@app.route("/collection")
@login_required
def collection():
  return render_template('collection.jinja2')


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
  create_default_users()
  return render_template("factory_reset.jinja2")


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