from .handlers import RouteHandler
from jupyter_server.extension.application import ExtensionApp
from traitlets import Unicode, Bool, List, Int
import pathlib
import os
import re

class ETCJupyterLabFeedbackApp(ExtensionApp):

    name = "etc_jupyterlab_feedback"

    nbgrader_validate_enabled = Bool(True, allow_none=False).tag(config=True)
    feedback_enabled = Bool(True, allow_none=False).tag(config=True)
    feedback_url = Unicode(None, allow_none=True).tag(config=True)
    nbgrader_validate_timeout = Int(5*60, allow_none=False).tag(config=True)
    feedback_timeout = Int(5*60, allow_none=False).tag(config=True)
    cert_path = Unicode(None, allow_none=True).tag(config=True)

    def initialize_settings(self):
        try:
            pass
        except Exception as e:
            self.log.error(str(e))
            raise e

    def initialize_handlers(self):
        try:
            self.handlers.extend([(r"/etc-jupyterlab-feedback/(.*)", RouteHandler)])
        except Exception as e:
            self.log.error(str(e))
            raise e
