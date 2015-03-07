from flask import Flask, session, render_template, request, redirect, g, flash
from flask_login import login_required, login_user, logout_user, current_user, LoginManager
from passlib.handlers.md5_crypt import md5_crypt
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from flask.ext.babel import Babel


app = Flask(__name__, instance_relative_config=False)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db?check_same_thread=False'
app.config['SQLALCHEMY_ECHO'] = False
db = SQLAlchemy(app)

# localization
babel = Babel(app)


from services.user_service import UserService
from models import *


def fmtDecimal(value):
  if isinstance(value, float):
    return float("{0:.2f}".format(value))
  return value


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

    return dict(settings=settings, sys_date=d, sys_time=t)


@app.route("/")
@login_required
def home():
  return render_template('home.jinja2')


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

import views.users
import views.collections
import views.settings
import views.system_setup
import views.rate_setup
import views.reports
import views.data_reset
