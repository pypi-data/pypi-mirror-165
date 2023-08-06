from functools import wraps
from typing import Callable, Iterable
from uuid import uuid4

from hashlib import md5
from flask import abort, Blueprint, Flask, request, session
from flask.config import Config

__all__ = ("CSRFProtection",)


class CSRFProtection:
    def __init__(self, app: Flask = None) -> None:
        self.app = app
        if not app is None:
            self.init_app(app)

        self.csrf_enabled: bool = True
        self.secret_key: bytes = None
        self.salt: bytes = None
        self.arg_names: Iterable = None
        self.cookie_names: Iterable = None
        self.header_names: Iterable = None
        self._invalid_token: Callable = None
        self._exempted_views: list[str] = []

    def init_app(self, app: Flask) -> None:
        self.app = app
        app.extensions["csrf_protection"] = self
        app.jinja_env.globals["gen_csrftoken"] = self.set_tokens

        self.load_config(app.config)

    def load_config(self, config: Config):
        self.arg_names = config.get("CSRF_ARG_NAMES", ("CSRF_TOKEN", "csrf_token",))
        self.cookie_names = config.get("CSRF_COOKIE_NAMES", ("CSRF_TOKEN", "csrf_token",))
        self.header_names = config.get("CSRF_HEADER_NAMES", ("X-CSRF-TOKEN", "X-CSRF-Token", "x-csrf-token",))
        self.csrf_enabled = config.get("CSRF_ENABLE", True)
        if not self.csrf_enabled:
            return
        self.secret_key = config.get("CSRF_SECRET_KEY", config.get("SECRET_KEY"))
        self.salt = config.get("CSRF_SALT")
        if self.secret_key is None:
            raise NotImplementedError("Missing secret key")
        if self.salt is None:
            self.salt = b"csrf-token"
        if isinstance(self.secret_key, str):
            self.secret_key = self.secret_key.encode("utf-8")
        if isinstance(self.salt, str):
            self.salt = self.salt.encode("utf-8")

    def invalid_token(self, callback: Callable):
        self._invalid_token = callback

    @property
    def invalid_token_handler(self) -> Callable:
        if self._invalid_token is None:
            abort(403)
        return self._invalid_token

    def get_client_token(self) -> str | None:
        token = None
        for name in self.arg_names:
            token = request.values.get(name)
            if not token is None:
                return token

        for name in self.cookie_names:
            token = request.cookies.get(name)
            if not token is None:
                return token

        for name in self.header_names:
            token = request.headers.get(name)
            if not token is None:
                return token

    def verify_token(self):
        if request.method == "GET" or not self.csrf_enabled:
            return None
        token = self.get_client_token()
        if token is None:
            return self.invalid_token_handler()
        elif not self.valid_token(token):
            return self.invalid_token_handler()

    def exempt_view(self, view: str | Callable):
        if isinstance(view, str):
            view_location = view
        else:
            view_location = f"{view.__module__}.{view.__name__}"
        self._exempted_views.append(view_location)

    def generate_tokens(self) -> tuple[bytes, str]:
        print(self.salt, self.secret_key)
        token = self.merge_token(
            self.salt, self.secret_key, uuid4().hex.encode("utf-8")
        )
        return token, md5(token).hexdigest()

    def protect_blueprint(self, bp: Blueprint):
        @bp.before_request
        def check_csrf():
            if request.method == "GET" or not self.csrf_enabled:
                return None
            view = self.app.view_functions.get(request.endpoint)
            dest = f"{view.__module__}.{view.__name__}"
            if dest in self._exempted_views:
                return
            return self.verify_token()

    def protect_blueprints(self, bps: list[Blueprint]):
        for bp in bps:
            self.protect_blueprint(bp)

    def set_tokens(self) -> str:
        server_token, token = self.generate_tokens()

        session["_csrf_token"] = server_token.decode("utf-8")

        return token

    def token_required(self, fn: Callable):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify = self.verify_token()
            if verify is None:
                return fn(*args, **kwargs)
            return verify

        return wrapper

    def valid_token(self, token) -> bool:
        server_token = session.get("_csrf_token")

        return md5(server_token.encode("utf-8")).hexdigest() == token

    @staticmethod
    def merge_token(*args):
        result: bytes = b""
        for arg in args:
            result += arg
        return result
