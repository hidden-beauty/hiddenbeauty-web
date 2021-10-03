import os
import json
from peewee import *
from werkzeug.exceptions import NotFound
from flask import Flask, render_template, flash, url_for, current_app, redirect, Blueprint, request, send_file
from hiddenbeauty.db_model import DBModel
from hiddenbeauty.utils import url_for_screenshot_m
import config

bp = Blueprint('index', __name__)


@bp.route('/index')
def soon():
    return redirect("/")

@bp.route('/robots.txt')
def robots():
    return render_template("robots.txt")

@bp.route('/favicon.ico')
def favicon():
    return send_file("../static/img/favicon-32x32.png")

def load_slide_models(slide_model_ids):
    slide_models = []
    for slide in slide_model_ids:
        m = DBModel.get(DBModel.model_id == slide[0], DBModel.code == slide[1], DBModel.version == slide[2])
        m.parse_data()

        slide_models.append({
            "desc" : "%s model %s" % (m.body_part, m.display_code),
            "screenshot" : url_for_screenshot_m(m, True, False),
            "link" : "/model/" + m.display_code
        })

    return slide_models

@bp.route('/')
def index():
    model_count = DBModel.select().count()
    models = DBModel.select(DBModel.model_id, DBModel.code, DBModel.body_part, DBModel.version) \
                    .order_by(DBModel.created.desc()) \
                    .limit(3)

    with open("static/stats/aggregated_stats.json", "r") as j:
        stats = json.loads(j.read())

    min_age = 1000
    max_age = 18
    for age in stats["ages"]:
        age = int(age)
        min_age = age if age < min_age else min_age
        max_age = age if age > max_age else max_age

    model_list = []
    for m in models:
        m.parse_data()
        model_list.append(m)

    sample_model_ids = [
        ("554268", "FSAN", "1"),
        ("628398", "FSAN", "1"),
        ("694420", "PLNN", "1"),
        ("191644", "VLAN", "1")
    ]
    sample_models = load_slide_models(sample_model_ids)

    picks_model_ids = [
        ("746625", "VLNP", "1"),
        ("352392", "PLNN", "1"),
        ("426060", "VLNP", "2"),
        ("591522", "FSAN", "5")
    ]
    picks_models = load_slide_models(picks_model_ids)

    return render_template("index.html", 
        sample_models=sample_models, 
        picks_models=picks_models, 
        recent_models=model_list, 
        model_count=model_count,
        min_age=min_age,
        max_age=max_age)


@bp.route('/browse')
def browse():
    return redirect(url_for("browse.by_part"))

@bp.route('/team')
def team():
    return render_template("about/team.html")

@bp.route('/about')
def about():
    return render_template("about/about.html")

@bp.route('/company')
def company():
    return render_template("about/company.html")

@bp.route('/contact')
def contact():
    return render_template("about/contact.html")

@bp.route('/privacy')
def privacy():
    return render_template("about/privacy.html")

@bp.route('/opensource')
def opensource():
    return render_template("about/opensource.html")
