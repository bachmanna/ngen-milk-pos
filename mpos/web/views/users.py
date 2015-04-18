from flask import render_template, request, redirect, g, flash, jsonify
from flask_login import login_required, current_user
from passlib.handlers.md5_crypt import md5_crypt

from web import app, admin_permission

from services.user_service import UserService
from models.User import User

@app.route("/user", methods=['GET', 'POST'])
@login_required
@admin_permission.require()
def manage_user():
  service = UserService()
  user = User(user_id="",name="")
  if request.method == 'POST':
    id = request.form["id"]
    name = request.form["name"]
    password = request.form["password"]
    if id and int(id):
      user = service.get(int(id))
      if name and len(name) > 3 and password and len(password) > 4:
        password = md5_crypt.encrypt(password)
        if service.update(id, name, password):
          flash("User update successfully!")
      elif name:
        flash("Password should be greater than 4 letters!", "error")
    else:
      flash("Invalid user id.", "error")

  user_list = service.search()
  return render_template("manage_user.jinja2", user=user, user_list=user_list)