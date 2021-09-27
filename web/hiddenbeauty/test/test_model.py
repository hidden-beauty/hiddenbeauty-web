import os
import flask_testing
from flask import url_for
from werkzeug.exceptions import BadRequest, InternalServerError, NotFound

from hiddenbeauty.app import app
from utils import ServerTestCase

class ModelViewsTestCase(ServerTestCase):

    def setUp(self):
        ServerTestCase.setUp(self)

    def test_model_root(self):
        resp = self.client.get(url_for('model.model_root'))
        self.assert200(resp)

    def test_model(self):
        resp = self.client.get(url_for('model.model', model="000000-HSNN"))
        self.assert200(resp)
