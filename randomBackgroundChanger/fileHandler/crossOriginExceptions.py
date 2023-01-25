
from abc import ABC


from werkzeug.exceptions import Unauthorized, TooManyRequests, BadRequest


class _CrossOriginExceptionMixin(ABC):

    def get_headers(self, environ=None, scope=None):
        headers = super().get_headers(environ=environ, scope=scope)
        headers.append(("Access-Control-Allow-Origin", "*"))
        return headers


class CrossOriginUnauthorised(_CrossOriginExceptionMixin, Unauthorized):
    pass


class CrossOriginBadRequest(_CrossOriginExceptionMixin, BadRequest):
    pass


class CrossOriginTooManyRequests(_CrossOriginExceptionMixin, TooManyRequests):
    pass
