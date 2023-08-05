import json
import traceback
from ._version import _fetchVersion
from requests import Session, Request
from jupyter_server.base.handlers import JupyterHandler
from jupyter_server.extension.handler import ExtensionHandlerMixin
import tornado
import urllib.request
from os.path import join, expanduser
import subprocess
from tornado.ioloop import IOLoop
import uuid

MACHINE_ID = str(uuid.uuid4())

class HTTPException(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message

class RouteHandler(ExtensionHandlerMixin, JupyterHandler):
    @tornado.web.authenticated
    def get(self, resource):
        try:
            self.set_header('content-type', 'application/json')
            if resource == 'config':
                self.finish(json.dumps({
                    'nbgrader_validate_enabled': self.extensionapp.nbgrader_validate_enabled,
                    'feedback_enabled': self.extensionapp.feedback_enabled,
                    'version':  _fetchVersion()
                }))
            else:
                self.set_status(404)

        except Exception as e:
            self.set_status(500)
            self.log.error(traceback.format_exc())


    @tornado.web.authenticated
    async def post(self, resource):
        try:
            if resource == 'nbgrader_validate' and self.extensionapp.nbgrader_validate_enabled == True:
                result = await IOLoop.current().run_in_executor(None, self.nbgrader_validate, self.get_json_body())
                self.set_header('content-type', 'application/json')
                self.set_status(200)
                self.finish(result)
            elif resource == 'feedback' and self.extensionapp.feedback_enabled == True:
                result = await IOLoop.current().run_in_executor(None, self.feedback, self.get_json_body())
                self.set_header('content-type', 'application/json')
                self.set_status(200)
                self.finish(result)
            else:
                self.set_status(404)

        except HTTPException as e:
            self.log.error(e.message)
            self.set_status(e.code)
            self.log.error(traceback.format_exc())
        except Exception as e:
            self.set_status(500)
            self.log.error(traceback.format_exc())

    def feedback(self, data):

        fullpath = expanduser(
            join(self.settings['server_root_dir'], data['notebook_path']))

        with open(fullpath, 'rb') as f:
            data = json.load(f)

            for cell in data['cells']:
                if 'outputs' in cell:
                    cell['outputs'] = []

            data['metadata']['etc_machine_id'] = MACHINE_ID

            data = json.dumps(data).encode('utf-8')

            with Session() as s:

                req = Request(
                    'POST',
                    self.extensionapp.feedback_url,
                    data=data,
                    headers={
                        'accept': 'application/json',
                        'content-type': 'application/json'
                    })

                prepped = s.prepare_request(req)

                if self.extensionapp.cert_path:
                    res = s.send(
                        prepped, 
                        proxies=urllib.request.getproxies(),
                        timeout=self.extensionapp.feedback_timeout,
                        verify=self.extensionapp.cert_path)
                else:
                    res = s.send(
                        prepped, 
                        proxies=urllib.request.getproxies(),
                        timeout=self.extensionapp.feedback_timeout
                        )

                return res.content.decode('utf-8')

    def nbgrader_validate(self, data):
        
        fullpath = expanduser(
            join(self.settings['server_root_dir'], data['notebook_path']))
        full_output = subprocess.run(
            ["nbgrader", "validate", fullpath], 
            capture_output=True,
            timeout=self.extensionapp.nbgrader_validate_timeout
            )
        output = full_output.stdout.decode(encoding='UTF-8')
        return json.dumps(output)

