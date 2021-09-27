import os
import flask_testing
from flask import url_for
from werkzeug.exceptions import BadRequest, InternalServerError, NotFound

from hiddenbeauty.app import app
from utils import ServerTestCase

class BrowseViewsTestCase(ServerTestCase):

    def setUp(self):
        ServerTestCase.setUp(self)

    def test_exhibit(self):
        resp = self.client.get(url_for('exhibit.index'))
        self.assert200(resp)
