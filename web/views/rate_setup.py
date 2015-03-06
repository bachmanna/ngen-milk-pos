from flask import render_template, request, redirect, g, flash
from flask_login import login_required

from web import app

from services.rate_service import RateService
from models import *


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