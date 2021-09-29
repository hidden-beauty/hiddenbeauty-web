import os
from werkzeug.exceptions import NotFound, InternalServerError
from flask import render_template,  url_for, Blueprint, send_file
from hiddenbeauty.kits import load_kit_list, make_kit_filename


bp = Blueprint('exhibit', __name__)

@bp.after_request
def noindex(response):
    response.headers['X-Robots-Tag'] = "noindex"
    return response


@bp.route('/')
def index():
    kits = load_kit_list()
    return render_template("exhibit/index.html", kits=kits)


@bp.route('/<slug>/download')
def dafadfsend_kit(slug):
    filename = make_kit_filename(slug)
    if not os.path.exists(filename):
        raise NotFound("Kit '%s' not found." % slug)

    return send_file(filename, attachment_filename=os.path.basename(filename), as_attachment=True)


@bp.route('/<slug>')
def exhibit(slug):
    kits = load_kit_list()
    for k in kits:
        if k['slug'] == slug:
            kit = k
            break
    else:
        raise NotFound("Exhibit '%s' not found." % slug)

    template = render_template("exhibit/exhibit-%s.html" % slug)
    if not template.startswith("<!--"):
        raise InternalServerError("exhibit template for '%s' does not start with a comment.")

    template_lines = template.split("\n")
    template_lines.pop(0)

    sections = []
    text = ""
    for line in template_lines:
        if line.startswith("<!--"):
           sections.append(text)
           text = ""
           continue
        text += line

    sections.append(text)

    for model, section in zip(kit['models'], sections):
        model['content'] = section

    footer = "\n".join(sections[len(kit['models']):])

    return render_template("exhibit/base.html", kit=kit, footer=footer)
