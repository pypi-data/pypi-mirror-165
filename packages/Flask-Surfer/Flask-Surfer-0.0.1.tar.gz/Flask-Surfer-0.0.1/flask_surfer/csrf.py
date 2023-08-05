from functools import wraps
from typing import Callable, Iterable
from uuid import uuid4

from hashlib import md5
from flask import abort, Blueprint, Flask, request, session

__all__ = ("CSRFProtection",)


class CSRFProtection:
    def __init__(self, app: Flask = None) -> None:
        self.app = app
        if not app is None:
            self.init_app(app)

        self.arg_names: Iterable = None
        self.header_names: Iterable = None
        self._invalid_token: Callable = None
        self._exempted_views: list[str] = []

    def init_app(self, app: Flask) -> None:
        self.app = app
        app.extensions["csrf_protection"] = self
        app.jinja_env.globals["gen_csrftoken"] = self.set_tokens

        self.arg_names = app.config.get("CSRF_ARG_NAMES", ("CSRF_TOKEN",))
        self.header_names = app.config.get("CSRF_HEADER_NAMES", ("X-CSRF-TOKEN"))

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

        for name in self.header_names:
            token = request.headers.get(name)
            if not token is None:
                return token

    def verify_token(self):
        if request.method == "GET":
            return
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

    def protect_blueprint(self, bp: Blueprint):
        @bp.before_request
        def check_csrf():
            if request.method == "GET":
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
        salt, server_token, token = self.generate_tokens()

        session["_csrf_salt"] = salt
        session["_csrf_token"] = server_token

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
        salt = session.get("_csrf_salt")
        server_token = session.get("_csrf_token")

        return (
            md5(self.merge_token(salt, server_token).encode("utf-8")).hexdigest()
            == token
        )

    @staticmethod
    def generate_tokens() -> tuple[str, str, str]:
        salt = uuid4().hex
        server_token = uuid4().hex
        token = md5(f"{server_token}-{salt}".encode("utf-8")).hexdigest()

        return salt, server_token, token

    @staticmethod
    def merge_token(salt: str, token: str):
        return f"{token}-{salt}"
