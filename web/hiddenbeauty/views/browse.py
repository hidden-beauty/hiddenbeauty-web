import os
import json
from shutil import copyfile, rmtree
import subprocess
from tempfile import mkdtemp
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError
from flask import Flask, render_template, flash, url_for, current_app, redirect, Blueprint, request, send_file
from hiddenbeauty.db_model import DBModel
import config


bp = Blueprint('browse', __name__)


@bp.route('/by-part')
def by_part():

    body_parts = DBModel.select(DBModel.body_part).distinct()
    body_parts = [ part.body_part for part in body_parts ]
    body_parts = sorted(body_parts, reverse=True)
    body_parts.remove("anatomical")

    models = DBModel.select().order_by(DBModel.body_part, DBModel.model_id, DBModel.code, DBModel.version)
    sections = {}
    for model in models:
        if model.model_id in '284284':
            continue
        model.parse_data()
        if not model.body_part in sections:
            sections[model.body_part] = { 'name' : model.body_part, 'models' : [] }
        sections[model.body_part]['models'].append(model)

    return render_template("browse/browse-by-part.html", order = body_parts, sections = sections)


@bp.route('/by-model')
def by_model():

    models = {}
    tag_counts = {}
    last_id = ""
    model_list = []
    model_tags = []
    for model in DBModel.select().order_by(DBModel.model_id, DBModel.code):
        if model.model_id == '284284':
            continue

        model.parse_data()
        model.common_tags_list = []

        if last_id and last_id != model.model_id:
            for tag in tag_counts:
                if len(model_list) == tag_counts[tag]:
                    model_tags.append(tag)
                    for m in model_list:
                        m.tags_list.remove(tag)

            for m in model_list:
                m.common_tags_list = model_tags

            model_list = []
            model_tags = []
            tag_counts = {}
            
        if not model.model_id in models:
            models[model.model_id] = []

        models[model.model_id].append(model)
      
        for tag in model.tags_list:
            try:
                tag_counts[tag] += 1
            except KeyError:
                tag_counts[tag] = 1

        last_id = model.model_id 
        model_list.append(model)



    model_list = sorted(models.keys())
    # Move the hand to the last item, feel wrong to have it be first
    if model_list[0] == "000000":
        model_list.append(model_list.pop(0))

    return render_template("browse/browse-by-model.html", models=models, model_list=model_list)


@bp.route('/by-attributes')
def by_attributes():

    keywords = (request.args.get('a') or "").split(",")
    keywords = [ k.lower() for k in keywords ]

    models = []
    for model in DBModel.select():
        if model.model_id == '284284':
            continue
        model.parse_data()
        models.append(model)

    info = {}
    tags = {}
    events = {}
    models_dict = {}
    for model in models:
        for tag in model.tags_list:
            if not tag:
                continue
            try:
                tags[tag].append(model.display_code)
            except KeyError:
                tags[tag] = [ model.display_code ]

        for event in model.history_list:
            if not event:
                continue
            try:
                events[event].append(model.display_code)
            except KeyError:
                events[event] = [ model.display_code ]

        if model.links:
            try:
                info['link'].append(model.display_code)
            except KeyError:
                info['link'] = [ model.display_code ]

        if model.comment:
            try:
                info['comment'].append(model.display_code)
            except KeyError:
                info['comment'] = [ model.display_code ]

        if model.excited != "not excited":
            try:
                info['excited'].append(model.display_code)
            except KeyError:
                info['excited'] = [ model.display_code ]

        models_dict[model.display_code] = model.to_json()

    tags_list = []
    disp_tags = []
    for tag in sorted(tags):
        tags_list.append((tag, tags[tag]))
        disp_tags.append((tag, True if tag in keywords else False))

    events_list = []
    disp_events = []
    for event in sorted(events):
        events_list.append((event, events[event]))
        disp_events.append((event, True if event in keywords else False))

    info_list = []
    disp_info = []
    for i in sorted(info):
        info_list.append((i, info[i]))
        disp_info.append((i, True if i in keywords else False))

    return render_template("browse/browse-by-attributes.html", 
        models=json.dumps(models_dict), 
        info=disp_info, info_list=json.dumps(info_list), 
        tags=disp_tags, tags_list=json.dumps(tags_list),
        events=disp_events, events_list=json.dumps(events_list))


@bp.route('/by-date')
def by_date():
    model_count = DBModel.select().count()
    models = DBModel.select() \
                    .order_by(DBModel.created.desc())
    model_list = []
    for model in models:
        if model.model_id in '284284':
            continue
        model.parse_data()
        model_list.append(model)

    return render_template("browse/browse-by-date.html", models=model_list)
