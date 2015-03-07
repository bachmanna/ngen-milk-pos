from flask import render_template, request, redirect, g, flash, url_for
from flask_login import login_required

from web import app

from services.member_service import MemberService
from services.rate_service import RateService
from configuration_manager import ConfigurationManager
from models import *

@app.route("/system_setup")
@login_required
def system_setup():
  return render_template("system_setup.jinja2")

@app.route("/language")
@login_required
def system_language():
  key = request.args.get('key', None)
  if key:
    settings = {}
    key = settings[SystemSettings.LANGUAGE] = "en" if key == "en" else "ta"

    configManager = ConfigurationManager()
    configManager.set_all_settings(settings)
    return redirect(url_for("system_language"))
  if not key:
    key = g.app_settings.get(SystemSettings.LANGUAGE, None)
  return render_template("language.jinja2",key=key)

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