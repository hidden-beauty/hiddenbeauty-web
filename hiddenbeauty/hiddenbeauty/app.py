import json
import os
import sys

from flask import Flask, render_template, flash, url_for, current_app, redirect, g, request
from flask_static_digest import FlaskStaticDigest
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.security import generate_password_hash, check_password_hash

from hiddenbeauty.db_model import db, DB_FILE
import hiddenbeauty.utils as utils
import config


STATIC_FOLDER = "../static"
TEMPLATE_FOLDER = "../template"

flask_static_digest = FlaskStaticDigest()

app = Flask(__name__,
            static_folder = STATIC_FOLDER, 
            template_folder = TEMPLATE_FOLDER)
app.config.from_object('config')
app.config['FONTAWESOME_SERVE_LOCAL'] = False
app.config['FLASK_STATIC_DIGEST'] = flask_static_digest

app.wsgi_app = ProxyFix(app.wsgi_app)

flask_static_digest.init_app(app)

db_file = os.path.join(config.MODEL_DIR, DB_FILE)
if not os.path.exists(db_file):
    print("WARNING: Cannot find models db: %s" % db_file)

db.init(db_file)


from hiddenbeauty.views.index import bp as index_bp
from hiddenbeauty.views.model import bp as model_bp
from hiddenbeauty.views.browse import bp as browse_bp
from hiddenbeauty.views.docs import bp as docs_bp
from hiddenbeauty.views.exhibit import bp as exhibit_bp
app.register_blueprint(index_bp)
app.register_blueprint(model_bp, url_prefix='/model')
app.register_blueprint(browse_bp, url_prefix='/browse')
app.register_blueprint(docs_bp, url_prefix='/docs')
app.register_blueprint(exhibit_bp, url_prefix='/exhibit')

app.jinja_env.globals.update(static_url=utils.static_url)
app.jinja_env.globals.update(url_for_screenshot=utils.url_for_screenshot)
app.jinja_env.globals.update(url_for_screenshot_m=utils.url_for_screenshot_m)

@app.before_request
def before_request_func():
    sfw = request.cookies.get('sfw')
    if sfw == "0":
        g.sfw = False
        g.sfw_js = "false"
    else:
        g.sfw = True
        g.sfw_js = "true"

@app.context_processor
def inject_domain():
    return dict(domain=config.SITE_DOMAIN)

@app.errorhandler(404)
def page_not_found(message):
    return render_template('errors/404.html', message=message), 404

@app.errorhandler(401)
def unauthorized(message):
    return render_template('errors/401.html', message=message), 401

@app.errorhandler(403)
def forbidden(message):
    return render_template('errors/401.html', message=message), 403

@app.errorhandler(500)
def internal_server_error(message):
    return render_template('errors/500.html', message=message), 500
