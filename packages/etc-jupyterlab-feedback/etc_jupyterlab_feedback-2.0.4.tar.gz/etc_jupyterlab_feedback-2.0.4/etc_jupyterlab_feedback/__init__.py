from ._version import __version__
from .application import ETCJupyterLabFeedbackApp
import json
from pathlib import Path

HERE = Path(__file__).parent.resolve()

with (HERE / "labextension" / "package.json").open() as fid:
    data = json.load(fid)


def _jupyter_labextension_paths():
    return [{
        "src": "labextension",
        "dest": data["name"]
    }]

def _jupyter_server_extension_points():
    return [{
        "module": "etc_jupyterlab_feedback",
        "app": ETCJupyterLabFeedbackApp
    }]

load_jupyter_server_extension = ETCJupyterLabFeedbackApp.load_classic_server_extension
