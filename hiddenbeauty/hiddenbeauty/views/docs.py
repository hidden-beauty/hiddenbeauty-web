import json
import os
from operator import itemgetter

from flask import Flask, render_template, Blueprint, send_file
from peewee import *
from hiddenbeauty.db_model import DBModel
import config


bp = Blueprint('docs', __name__)

@bp.after_request
def noindex(response):
    response.headers['X-Robots-Tag'] = "noindex"
    return response

@bp.route('/printing-guide')
def printing_guide():
    return render_template("docs/printing-guide.html")

@bp.route('/model-codes')
def model_codes():
    return render_template("docs/model-codes.html")

@bp.route('/faq')
def faq():
    return render_template("docs/faq.html")

@bp.route('/guide')
def guide():
    return render_template("docs/illustrated-guide.html")

@bp.route('/model-diversity')
def diversity():
    return render_template("docs/model-diversity.html")

@bp.route('/statistics')
def statistics():
    model_stats = []
    for model in DBModel.select(DBModel.body_part,fn.COUNT(DBModel.id).alias('ct')).group_by(DBModel.body_part):
        if model.body_part == 'anatomical':
            continue

        model_stats.append((model.body_part, model.ct))

    model_stats = sorted(model_stats, key=itemgetter(1), reverse=True)
    total_models = DBModel.select().count()
    total_models -= 1  # remove the anatomical from the count

    with open("static/stats/aggregated_stats.json", "r") as j:
        jsdoc = j.read()

    stats = json.loads(jsdoc)

    ages = []
    for age in stats["ages"]:
        ages.append(( age, stats["ages"][age] ))

    countries = []
    for country in stats["countries"]:
        countries.append(( country, int(stats["countries"][country]) ))
    countries = sorted(countries, key=itemgetter(1,0), reverse=True)

    ethnicities = []
    for ethnicity in stats["ethnicities"]:
        ethnicities.append(( ethnicity, stats["ethnicities"][ethnicity] ))
    ethnicities = sorted(ethnicities, key=itemgetter(1,0), reverse=True)

    return render_template("docs/statistics.html", 
        model_stats=model_stats,
        total_models=total_models,
        ages=ages,
        countries=countries,
        ethnicities=ethnicities)
