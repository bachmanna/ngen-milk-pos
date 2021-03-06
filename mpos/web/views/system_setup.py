from flask import render_template, request, redirect, g, flash, url_for
from flask_login import login_required, current_user
from flask_babel import lazy_gettext, gettext
from datetime import datetime

from web import app, get_backup_directory

from services.member_service import MemberService
from services.rate_service import RateService
from services.export_import_service import ExportImportService
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
  member = None
  if request.method == 'POST':
    try:
      code = request.form.get("code")
      name = request.form.get("name")
      mobile = request.form.get("mobile")
      cattle_type = request.form.get("cattle_type")
      if code and int(code):
        id = int(code)
        member = member_service.get(id)
        if name and len(name) > 1 and len(cattle_type) > 0 and len(mobile) > 0:
          if len(mobile) != 10:
            flash("Invalid mobile number, must be 10 digits",category="error")
          else:
            if not member:
              user_id = current_user.id
              member_service.add(name, cattle_type, mobile, user_id, datetime.now(), _id=id)
            else:
              member_service.update(id, name, cattle_type, mobile)
            member = None
            flash("Member saved successfully!")
        else:
            flash("Invalid member name and mobile number!", category="error")
      else:
        flash("Invalid member data.",category="error")
    except Exception as e:
      print e
      flash(e, category="error")

  member_list = member_service.search()
  free_list = []
  used_list = [int(x.id) for x in member_list]
  for i in range(1,1000):
    if len(free_list) > 10:
        break
    if i not in used_list:
      free_list.append(str(i))

  if not member:
    member = {}
  return render_template("member.jinja2",member_list=member_list, free_list=free_list, member=member)


@app.route("/member_export")
@login_required
def member_export():
  service = ExportImportService(Member.__table__)
  if service.do_export():
    flash(str(lazy_gettext("Export successfull!")))
  else:
    flash(str(lazy_gettext("Import failed!")), "error")
  return redirect("/member")


@app.route("/member_import")
@login_required
def member_import():
  service = ExportImportService(Member.__table__)
  if service.do_import():
    flash(str(lazy_gettext("Import successfull!")))
  else:
    flash(str(lazy_gettext("Import failed!")), "error")
  return redirect("/member")
