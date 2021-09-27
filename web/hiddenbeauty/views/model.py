import base64
import json
import gzip
import os
import random
import requests
from subprocess import run, CalledProcessError
import tempfile
import urllib
from zipfile import ZipFile

from PIL import Image
from peewee import *
from werkzeug.exceptions import BadRequest, NotFound, ServiceUnavailable
from flask import Flask, render_template, flash, url_for, current_app, redirect, Blueprint, request, send_file, Response, make_response
from hurry.filesize import size, alternative
from hiddenbeauty.db_model import DBModel
import config

FONT_FILE = "admin/font/d-din-exp.ttf"
BOLD_FONT_FILE = "admin/font/d-din-bold.ttf"
MAX_NUM_RELATED_MODELS = 3

bp = Blueprint('model', __name__)

@bp.route('/m/<path:filename>')
def send_model(filename):
    if current_app.debug and filename.endswith(".stl"):
        filename = os.path.join(current_app.config['MODEL_DIR'], filename + ".gz")
        if not os.path.exists(filename):
            raise NotFound()

        with gzip.open(filename, 'rb') as f:
            content = f.read()

        response = Response(content, status=200)
        response.headers['Content-Length'] = len(content)
        response.headers['Content-Type'] = 'model/stl'
        return response


    if not filename.endswith(".stl"):
        return send_file(os.path.join(current_app.config['MODEL_DIR'], filename))

    gz_filename = os.path.join(current_app.config['MODEL_DIR'], filename + ".gz")
    try:
        with open(gz_filename, "rb") as f:
            content = f.read()
    except IOError as err:
        raise NotFound("file '%s' not found." % filename)

    response = Response(content, status=200)
    response.headers['Content-Length'] = len(content)
    response.headers['Content-Type'] = 'model/stl'
    response.headers['Content-Encoding'] = 'gzip'
    return response


@bp.route('/m/<path:filename>/u')
def send_model_uncompressed(filename):
    if current_app.debug and filename.endswith(".stl"):
        filename = os.path.join(current_app.config['MODEL_DIR'], filename + ".gz")
        if not os.path.exists(filename):
            raise NotFound()

        with gzip.open(filename, 'rb') as f:
            content = f.read()

        response = Response(content, status=200)
        response.headers['Content-Length'] = len(content)
        response.headers['Content-Type'] = 'model/stl'
        return response


    if not filename.endswith(".stl"):
        return send_file(os.path.join(current_app.config['MODEL_DIR'], filename))

    gz_filename = os.path.join(current_app.config['MODEL_DIR'], filename + ".gz")
    try:
        with gzip.open(gz_filename, 'rb') as f:
            content = f.read()
    except IOError as err:
        raise NotFound("file '%s' not found." % filename)

    response = Response(content, status=200)
    response.headers['Content-Length'] = len(content)
    response.headers['Content-Type'] = 'model/stl'
    return response


@bp.route('/<model>/upload')
def upload_model(model):

    try:
        id, code, version = model.split("-")
    except ValueError:
        id, code = model.split("-")
        version = "1"
        
    solid_file = "%s-%s-%s-solid.stl" % (id, code, version)
    solid_path = "/%s/%s/%s" % (id, code, solid_file)

    if config.STL_BASE_URL:
        url = config.config.STL_BASE_URL + "/model/m" + solid_path
    else:
        url = "https://" + config.SITE_DOMAIN + "/model/m" + solid_path
    data = {
        "items": [
            {
               "modelUrl": url,
               "quantity": 1,
               "unit": "mm"
            }
        ]
    }
    r = requests.post('https://api.craftcloud3d.com/configuration', json=data, headers={ "use-model-urls": "true" })
    if not r.ok:
        print("Calling craftcloud failed: %s '%s'" % (r.status_code, r.text))
        return make_response("Could not upload model to craft cloud servers. Please try again later."), 503

    return Response(r.json()['configurationId'], status=200)


@bp.route('/')
def model_root():
    return render_template("error.html")


@bp.route('/<model>')
def model(model):
    return prepare_model(model, current_app.config["SUBMIT_SCREENSHOTS"])


@bp.route('/<model>/solid')
def model_solid(model):
    return prepare_model(model, current_app.config["SUBMIT_SCREENSHOTS"], True)


@bp.route('/<model>/screenshot')
def model_screenshot_get(model):
    return prepare_model(model, True)


@bp.route('/<id>-<code>-<int:version>/screenshot', methods = ['POST'])
def model_screenshot_post(id, code, version):
    if not config.SUBMIT_SCREENSHOTS:
        raise NotFound()

    fh, tmp_img = tempfile.mkstemp()
    os.close(fh)

    fh, tmp_img2 = tempfile.mkstemp()
    os.close(fh)

    fn = os.path.join(config.MODEL_DIR, id, code, "%s-%s-%d-screenshot.jpg" % (id, code, version))
    tagged = os.path.join(config.MODEL_DIR, id, code, "%s-%s-%d-screenshot-tagged.jpg" % (id, code, version))

    data = base64.b64decode(request.get_data()[23:])
    with open(tmp_img, "wb") as f:
        f.write(data)

    # TODO: Improve error handling here
    try:
        run(['convert',  
            tmp_img,
            "-resize", "800x800",
            fn], check=True)
    except CalledProcessError as err:
        print(err.output)

    if version > 1:
        model_code = "%s-%s-%s" % (id, code, version)
    else:
        model_code = "%s-%s" % (id, code)

    try:
        run(['convert',  
            fn,
            "-gravity", "north",
            "-background", "#F2ECE5",
            "-extent", "%dx%d" % (800, 850),
            tmp_img], check=True)
        run(['convert',  
            tmp_img,
            "-pointsize", "28", 
            "-font", FONT_FILE, 
            "-fill", "black", 
            "-gravity", "southwest",
            "-draw", 'text 8,3 "%s"' % (model_code), 
            "-pointsize", "28", 
            "-fill", "#bbbbbb", 
            "-gravity", "southeast",
            "-rotate", "90",
            "-font", BOLD_FONT_FILE, 
            "-pointsize", "36", 
            "-draw", 'text 10,5 "https://hiddenbeauty.ch"', 
            "-rotate", "-90",
            tmp_img2], check=True)
        run(['convert',  
            tmp_img2,
            "static/img/watermark.png",
            "-gravity", "southeast",
            "-geometry", "+5-0",
            "-composite",
            tagged], check=True)
        os.unlink(tmp_img)
        os.unlink(tmp_img2)
    except CalledProcessError as err:
        print(err.output)

    return ""


def get_related_models(model):

    desc = ""
    models = DBModel.select(DBModel.model_id, DBModel.code, DBModel.body_part, DBModel.version) \
                    .where(DBModel.model_id == model.model_id, DBModel.code != model.code).limit(3)
    models = [ m for m in models ]

    if len(models):
        desc = "more models from the same person"
    if len(models) >= MAX_NUM_RELATED_MODELS:
        [ m.parse_data() for m in models ]
        return { "desc" : desc, "models" : models[0:MAX_NUM_RELATED_MODELS] }

    same_part_models = DBModel.select(DBModel.model_id, DBModel.code, DBModel.body_part, DBModel.version) \
                              .where(DBModel.body_part == model.body_part, DBModel.model_id != model.model_id)
    same_part_models = [ m for m in same_part_models ]
    random.shuffle(same_part_models)

    if len(same_part_models):
        if len(models):
            desc += " and "
        models.extend(same_part_models)

    desc += "more %s models" % model.body_part
    [ m.parse_data() for m in models ]
    return { "desc" : desc, "models" : models[0:MAX_NUM_RELATED_MODELS] }


def prepare_model(model_code, screenshot, solid = False):

    if model_code.isdigit() and len(model_code) == 6:
        models = DBModel.select() \
                        .where(DBModel.model_id == model_code) \
                        .order_by(DBModel.body_part, DBModel.model_id, DBModel.code, DBModel.version)
        model_list = [ ]
        for m in models:
            m.parse_data()
            model_list.append(m)

        if not model_list:
            raise NotFound("Model %s does not exist." % model_code)

        if len(model_list) == 1:
            return redirect(url_for("model.model", model=model_list[0].model_id + '-' + model_list[0].code))
        else:
            model_list = [ m for m in models ]
            return render_template("docs/model-disambig.html", model=model_code, model_list=model_list)

    try:
        parts = model_code.split('-')
        if len(parts) == 3:
            id, code, version = parts
        else:
            id, code = parts
            version = 1
    except ValueError as err:
        raise NotFound("Invalid model id/code.")

    try:
        model = DBModel.get(DBModel.model_id == id, DBModel.code == code, DBModel.version == version)
    except Exception:
        raise NotFound("model %s does not exist." % model_code)

    model.parse_data()
    id = model.model_id
    code = model.code
    version = model.version
    model_file_med = config.STL_BASE_URL + "/model/m/%s/%s/%s-%s-%d-surface-med.stl" % (id, code, id, code, version)
    model_file_low = config.STL_BASE_URL + "/model/m/%s/%s/%s-%s-%d-surface-low.stl" % (id, code, id, code, version)
    model_file_solid= config.STL_BASE_URL + "/model/m/%s/%s/%s-%s-%d-solid.stl" % (id, code, id, code, version)

    solid_file = "%s-%s-%d-solid.stl" % (id, code, version)
    solid_path = "/%s/%s/%s" % (id, code, solid_file)
    surface_file = "%s-%s-%d-surface.stl" % (id, code, version)
    surface_path = "/%s/%s/%s" % (id, code, surface_file)

    solid_size = os.path.getsize(config.MODEL_DIR + solid_path + ".gz")
    surface_size = os.path.getsize(config.MODEL_DIR + surface_path + ".gz")

    downloads = {
        'solid' : (size(solid_size, system=alternative), config.STL_BASE_URL + "/model/m" + solid_path, solid_file),
        'surface' : (size(surface_size, system=alternative), config.STL_BASE_URL + "/model/m" + surface_path, surface_file)
    }

    share_text = "Check out this 3D model of a human from Hidden Beauty (@quatschunfug):\n\n%s: %s. \n\n%s" % \
        (model.display_code, model.threed_model_description(), "https://hiddenbeauty.ch" + request.path)

    if current_app.debug:
        base_url = "http://localhost"
    else:
        base_url = "https://" + config.SITE_DOMAIN

    temp = render_template("browse/view.html", 
        model = model, 
        model_file_med=model_file_med, 
        model_file_low=model_file_low, 
        model_file_solid=model_file_solid, 
        screenshot = int(screenshot),
        downloads = downloads,
        solid=(1 if solid else 0),
        related = get_related_models(model),
        base_url=base_url,
        share_text=urllib.parse.quote(share_text))

    r = make_response(temp)
    r.headers.set('Access-Control-Allow-Origin', 'api.craftcloud3d.com')
    r.headers.set('Access-Control-Allow-Headers', 'use-model-urls')
    return r
