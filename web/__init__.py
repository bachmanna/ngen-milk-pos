from flask import Flask, session, render_template, request, redirect, g, flash
from flask_login import login_required, login_user, logout_user, current_user, LoginManager
from passlib.handlers.md5_crypt import md5_crypt
from pony.orm import sql_debug, db_session

app = Flask(__name__, instance_relative_config=False)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

from models import *

sql_debug(False)
db.generate_mapping(create_tables=True)

app.wsgi_app = db_session(app.wsgi_app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"
login_manager.login_message = None

from models.User import User
user_list = {1: User(user_id=1, name='User1', email='User1@milkpos.com', roles=['user']),
             2: User(user_id=2, name='User2', email='User2@milkpos.com', roles=['user']),
             3: User(user_id=3, name='SettingsUser', email='SettingsUser@milkpos.com', roles=['setting']),
             4: User(user_id=4, name='SuperAdmin', email='SuperAdmin@milkpos.com', roles=['admin'])}

user_hash_pass = {"$1$yWq10SD.$WQlvdj6kmHOY9KjHhuIGn1": 1,
                  "$1$Ii9Edtkd$cpxJMzTgpCmFxEhka2nKs/": 2,
                  "$1$P/A0YAOn$O8SuzMiowBVJAorhfY239/": 3,
                  "$1$doG2/gED$vTLr/Iob7T9z0.nydnJxD1": 4}


@login_manager.user_loader
def get_user(id):
    return user_list.get(int(id), None)


@app.before_request
def set_user_on_request_g():
    setattr(g, 'user', current_user)


@app.route("/")
@login_required
def home():
    return render_template('home.jinja2')


@app.context_processor
def settings_provider():
    from configuration_manager import ConfigurationManager
    config_manager = ConfigurationManager()
    settings = config_manager.get_all_settings()
    return dict(settings=settings)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form["password"]
        for phash in user_hash_pass.keys():
            user_id = user_hash_pass.get(phash)
            user = user_list.get(user_id)
            if md5_crypt.verify(password, phash) and user is not None:
                login_user(user, remember=False)
                return redirect("/")
        flash("Invalid password!")
    return render_template('login.jinja2')


@app.route('/logout')
@app.route('/logout/')
def app_logout():
    logout_user()
    session.clear()
    return redirect('/')