from flask import render_template, request, redirect, g, flash
from flask_login import login_required

from web import app


@app.route("/data_reset")
@login_required
def data_reset():
  return render_template("data_reset.jinja2")


@app.route("/factory_reset")
@login_required
def factory_reset():
  return render_template("factory_reset.jinja2")