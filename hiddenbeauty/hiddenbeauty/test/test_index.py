import os
import flask_testing
from flask import url_for
from werkzeug.exceptions import BadRequest, InternalServerError, NotFound

from hiddenbeauty.app import app
from utils import ServerTestCase

class IndexViewsTestCase(ServerTestCase):

    def setUp(self):
        ServerTestCase.setUp(self)

    def test_index(self):
        resp = self.client.get(url_for('index.index'))
        self.assert200(resp)

    def test_browse(self):
        resp = self.client.get(url_for('index.browse'))
        self.assert_redirects(resp, url_for('browse.by_part'))

    def test_about(self):
        resp = self.client.get(url_for('index.about'))
        self.assert200(resp)

    def test_company(self):
        resp = self.client.get(url_for('index.company'))
        self.assert200(resp)

    def test_contact(self):
        resp = self.client.get(url_for('index.contact'))
        self.assert200(resp)

    def test_support(self):
        resp = self.client.get(url_for('index.support'))
        self.assert200(resp)

    def test_support_success(self):
        resp = self.client.get(url_for('index.support_success'))
        self.assert200(resp)

    def test_support_cancel(self):
        resp = self.client.get(url_for('index.support_cancel'))
        self.assert200(resp)

    def test_donate(self):
        resp = self.client.get(url_for('index.donate'))
        self.assert_redirects(resp, url_for('index.support'))

    def test_privacy(self):
        resp = self.client.get(url_for('index.privacy'))
        self.assert200(resp)
