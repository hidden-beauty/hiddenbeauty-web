import flask_testing
from hiddenbeauty.app import app

class ServerTestCase(flask_testing.TestCase):

    def create_app(self):
        return app
