from flask import current_app

import config


def static_url(filename):
    return config.STATIC_BASE_URL + current_app.config['FLASK_STATIC_DIGEST'].static_url_for('static', filename=filename)

def url_for_screenshot(id, code, version):
    return config.IMAGE_BASE_URL + "/model/m/%s/%s/%s-%s-%d-screenshot.jpg" % (id, code, id, code, version)

def url_for_screenshot_m(model):
    return config.IMAGE_BASE_URL + "/model/m/%s/%s/%s-%s-%d-screenshot.jpg" % (model.model_id, model.code, model.model_id, model.code, model.version)

def url_for_tagged_screenshot(id, code, version):
    return config.IMAGE_BASE_URL + "/model/m/%s/%s/%s-%s-%d-screenshot-tagged.jpg" % (id, code, id, code, version)

def url_for_tagged_screenshot_m(model):
    return config.IMAGE_BASE_URL + "/model/m/%s/%s/%s-%s-%d-screenshot-tagged.jpg" % (model.model_id, model.code, model.model_id, model.code, model.version)
