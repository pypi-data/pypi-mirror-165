import json
import os

import tornado
from notebook.base.handlers import IPythonHandler
from notebook.utils import url_path_join

from urllib.parse import urlencode, unquote

class AppHandler(IPythonHandler):
  """Thin wrapper around the IPython handler which injects common properties."""
  @property
  def config(self):
      return self.settings["sn_config"]

class ConfigurationEndpointHandler(AppHandler):
  """
  Route handler for the /skillsnetwork-authoring-extension/config endpoint.

  A single endpoint that returns the Atlas base URL.
  """
  def get(self) -> None:
    print('test', type(self.config))
    self.finish({"ATLAS_BASE_URL": self.config.atlas_base_url, "SN_FILE_LIBRARY_URL": self.config.sn_file_library_url})


def setup_handlers(web_app, url_path: str) -> None:
  """Setup handlers in the jupyter server web app.

  Args:
    - web_app: Jupyter server web application instance to add handlers to.
    - url_path: Root url path for handlers.
  """
  host_pattern = ".*$"
  base_url = web_app.settings["base_url"]

  # Prepend the base_url so that it works in a JupyterHub setting
  handler_url_path = url_path_join(base_url, url_path)
  handlers = [
    (url_path_join(handler_url_path, "config"), ConfigurationEndpointHandler)
  ]
  web_app.add_handlers(host_pattern, handlers)
