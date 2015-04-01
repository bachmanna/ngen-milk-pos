from flask import Flask, session, render_template, request, redirect, g, flash, current_app, jsonify
from flask import make_response, Response
from flask_login import login_required, login_user, logout_user, current_user, LoginManager
from flask_principal import Principal, Permission, RoleNeed, UserNeed, AnonymousIdentity
from flask_principal import identity_changed, identity_loaded, Identity, PermissionDenied

from passlib.handlers.md5_crypt import md5_crypt
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_babel import Babel
import babel.numbers as bn
import os
import sys


app = Flask(__name__, instance_relative_config=False)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db') + '?check_same_thread=False'
app.config['SQLALCHEMY_ECHO'] = False
db = SQLAlchemy(app)

# localization
babel = Babel(app)

# authorization
principals = Principal(app)

# Create a permission with a single Need, in this case a RoleNeed.
basic_permission = Permission(RoleNeed('basic'))
setup_permission = Permission(RoleNeed('setup'))
data_permission = Permission(RoleNeed('data'))
admin_permission = Permission(RoleNeed('admin'))

role_permission_list = { "basic": basic_permission, "setup": setup_permission,
                         "data": data_permission, "admin": admin_permission}

def can_access(role):
  return role in role_permission_list and role_permission_list[role].can()

app.jinja_env.globals.update(can_access=can_access)


from services.user_service import UserService
from models import *


def fmtDecimal(value):
  if isinstance(value, float):
    return float("{0:.2f}".format(value))
  return value


def format_currency(value):
  formatted_value = bn.format_currency(value, "INR", locale="ta_IN")
  return formatted_value

def get_currency_symbol():
  return bn.get_currency_symbol('INR', locale='ta_IN')


login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"
login_manager.login_message = None

from models.User import User
from configuration_manager import ConfigurationManager

@app.errorhandler(PermissionDenied)
def handle_invalid_usage(error):
    return render_template("unauthorized.jinja2"), 403

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    # Assuming the User model has a list of roles, update the
    # identity with the roles that the user provides
    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role))

@babel.localeselector
def get_locale():
  return g.get('current_lang', 'en')

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
  setattr(g, 'current_lang', settings.get(SystemSettings.LANGUAGE, "en"))


@app.context_processor
def settings_provider():
    settings = g.app_settings

    d = datetime.now().strftime("%d/%m/%Y")
    t = datetime.now().strftime("%I:%M%p")

    return dict(settings=settings, sys_date=d, sys_time=t)


@app.route("/")
@login_required
def home():
  return render_template('home.jinja2')


@app.route("/login", methods=['GET', 'POST'])
def login():
  service = UserService()
  lst_users = service.search()
  username = ""
  if request.method == 'POST':
      username = request.form["username"]
      password = request.form["password"]
      if username and password and len(password) > 4:
        users = service.search(name=username)
        if users and len(users) == 1 and md5_crypt.verify(password, users[0].password):
          dbuser = users[0]
          user = User(user_id=dbuser.id, name=dbuser.name, email=dbuser.email, roles=dbuser.roles.split(","))
          login_user(user, remember=False)
          # Tell Flask-Principal the identity changed
          identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.id))
          return redirect("/")
      flash("Invalid password!")
  return render_template('login.jinja2', username=username, users=lst_users)


@app.route('/logout')
@app.route('/logout/')
def app_logout():
  logout_user()
  # Remove session keys set by Flask-Principal
  for key in ('identity.name', 'identity.auth_type'):
      session.pop(key, None)

  # Tell Flask-Principal the user is anonymous
  identity_changed.send(current_app._get_current_object(),
                        identity=AnonymousIdentity())
  session.clear()
  return redirect('/')


@app.route('/shutdown')
def app_shutdown():
  if sys.platform == 'linux2':
    #os.system("sudo shutdown now -h")
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output
  return render_template('shutdown.jinja2')


def is_usb_storage_connected():
  return os.path.exists("/dev/sda1") and os.path.ismount("/home/pi/usbdrv/")


def get_backup_directory():
  filename = 'backup'
  directory = os.path.join(app.root_path, filename)

  if is_usb_storage_connected():
    directory = os.path.join("/home/pi/usbdrv/", filename)

  if not os.path.exists(directory):
    os.makedirs(directory)
  return directory

import views.users
import views.collections
import views.settings
import views.system_setup
import views.rate_setup
import views.reports
import views.data_reset
