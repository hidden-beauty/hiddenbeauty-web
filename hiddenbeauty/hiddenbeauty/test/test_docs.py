import os
import flask_testing
from flask import url_for
from werkzeug.exceptions import BadRequest, InternalServerError, NotFound

from hiddenbeauty.app import app
from utils import ServerTestCase

class DocsViewsTestCase(ServerTestCase):

    def setUp(self):
        ServerTestCase.setUp(self)

    def test_printing_guide(self):
        resp = self.client.get(url_for('docs.printing_guide'))
        self.assert200(resp)

    def test_model_codes(self):
        resp = self.client.get(url_for('docs.model_codes'))
        self.assert200(resp)

    def test_faq(self):
        resp = self.client.get(url_for('docs.faq'))
        self.assert200(resp)

    def test_model_diversity(self):
        resp = self.client.get(url_for('docs.diversity'))
        self.assert200(resp)

    def test_statistics(self):
        resp = self.client.get(url_for('docs.statistics'))
        self.assert200(resp)

    def test_guide(self):
        resp = self.client.get(url_for('docs.guide'))
        self.assert200(resp)
