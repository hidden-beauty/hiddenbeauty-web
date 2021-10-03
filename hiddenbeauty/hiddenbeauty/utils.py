from flask import current_app

import config


def static_url(filename):
    return config.STATIC_BASE_URL + current_app.config['FLASK_STATIC_DIGEST'].static_url_for('static', filename=filename)

def url_for_screenshot(id, code, version, sfw, tagged):
    s = "-sfw" if sfw else ""
    t = "-tagged" if tagged else ""
    return config.IMAGE_BASE_URL + "/model/m/%s/%s/%s-%s-%d-screenshot%s%s.jpg" % (id, code, id, code, version, s, t)

def url_for_screenshot_m(model, sfw, tagged):
    s = "-sfw" if sfw else ""
    t = "-tagged" if tagged else ""
    return config.IMAGE_BASE_URL + "/model/m/%s/%s/%s-%s-%d-screenshot%s%s.jpg" % (model.model_id, model.code, model.model_id, model.code, model.version, s, t)
