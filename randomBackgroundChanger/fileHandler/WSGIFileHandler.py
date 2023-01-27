
from abc import ABC, abstractmethod

from gunicorn.app.base import BaseApplication


class GunicornBase(ABC, BaseApplication):

    def __init__(self, application):
        self._application = application
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self._application.app

    @property
    @abstractmethod
    def options(self):
        pass


class WSGIFileHandler(GunicornBase):

    @property
    def options(self):
        return {
            "bind": f"0.0.0.0:5000",
            "workers": 1,
            "worker_class": "eventlet"
        }
