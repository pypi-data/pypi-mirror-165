"""Spec types."""

from __future__ import annotations

import asyncio

from enum import Enum
from pathlib import Path as PPath
from pydantic import BaseSettings as UserSettings
from dataclasses import dataclass, field
from logging import getLogger

from typing import (
    Any,
    Callable,
    Dict,
    Literal,
    Type,
    Tuple,
    Optional,
    Sequence,
    Union,
)
from threading import Lock
from aiocronjob import Manager as CronManager
from fastapi.routing import APIRouter as Router, APIRoute as Route
from fastapi.openapi.utils import OpenAPI, get_openapi
from fastapi.datastructures import Headers
from fastapi import (
    FastAPI as Api,
    datastructures,
    Request,
    Header,
    Path,
    Body,
    Cookie,
    Query,
    Depends,
    Form,
    File,
)
from fastapi.responses import (
    JSONResponse,
    UJSONResponse,
    ORJSONResponse,
    RedirectResponse,
    HTMLResponse,
    StreamingResponse,
    PlainTextResponse,
    FileResponse,
    Response,
)

from poetry.core.pyproject import PyProjectTOML as PyProject
from fastapi.middleware import Middleware

from spec import fn, exception as exc_type  # noqa
from spec.loader import load_spec, load_i18n

log = getLogger(__name__)

AsyncIOErrors = (
    asyncio.CancelledError,
    asyncio.IncompleteReadError,
    asyncio.InvalidStateError,
    asyncio.TimeoutError,
)

ModuleSettings = Union[Dict, None]

_keep_thread = Lock()

_PLUGIN_REGISTRY = {}


class Environment(str, Enum):
    """Service environment.

    Relevant to the git branch name usually.
    Using for logging conditions, sentry environment, etc.
    """

    unknown = 'unknown'

    testing = 'testing'
    develop = 'develop'

    stage = 'stage'
    pre_stage = 'pre-stage'

    production = 'production'
    pre_production = 'pre-production'

    def dont_care_secrets(self) -> bool:
        """If is unimportant by secrets or others."""
        return self in (
            Environment.stage,
            Environment.pre_stage,
            Environment.develop,
            Environment.testing,
            Environment.unknown,
        )


@dataclass(frozen=True)
class URI:
    """Service uri."""

    host: str
    port: int
    scheme: str


@dataclass(frozen=True)
class Status:
    """Service status."""

    debug: bool
    testing: bool
    on_k8s: bool


@dataclass(frozen=True)
class Path:
    """Service paths."""

    app: PPath
    temp: PPath

    assets: PPath
    static: PPath
    media: PPath
    i18n: PPath

    pyproject: PPath
    log_config_name: Optional[str]
    log_config_path: Optional[PPath]


@dataclass(frozen=True)
class Service:
    """Service  params."""

    uri: URI
    entrypoint: str

    name: str

    # from poetry config
    tech_name: str
    tech_description: str
    tech_version: str


@dataclass(frozen=True)
class Policies:
    """Service policies."""

    service_workers: int

    db_pool_size: int
    db_max_connections: int

    request_timeout: int
    request_retry_max: int


@dataclass(frozen=True)
class I18N:
    """Service i18n localizations."""

    lang: str

    support_codes: Sequence[str]
    all_codes: Sequence[str]

    locales: Sequence[str]


@dataclass(frozen=True)
class ApiDoc:
    """Service api doc options."""

    prefix: str
    enabled: bool
    blm: bool


def literal_languages() -> Tuple:
    """Literal languages."""
    params = load_i18n()
    return tuple(params.all_codes)


Lang = Literal[literal_languages()]  # noqa


@dataclass(frozen=True)
class Profile:
    """Service profiling options."""

    log_level: str
    sentry_dsn: Optional[str] = None


@dataclass(frozen=True)
class Spec:
    """Service spec."""

    service: Service
    environment: Environment
    status: Status

    path: Path
    pyproject: PyProject

    policies: Policies
    i18n: I18N
    api_doc: ApiDoc

    profile: Profile

    def as_dict(self) -> Dict[str, Any]:
        """Spec as dict."""
        return {
            'pyproject': self.pyproject,
            'environment': self.environment,
            'service': self.service,
            'status': self.status,
            'path': self.path,
            'policies': self.policies,
            'api_doc': self.api_doc,
            'i18n': self.i18n,
            'profile': self.profile,
        }


class ServiceMixin:
    """Service mixin."""

    spec: Spec

    i18n: Callable = None
    cron: Type[CronManager] = None
    settings: Type[UserSettings] = None
    modules: Dict[str, Module] = None


class App(Api, ServiceMixin):
    """App."""

    pass


class InjectMiddleware:
    """Module inject middleware."""

    __slots__ = 'app',

    module: Module = None

    def __init__(self, app):
        """Init middleware."""
        self.app = app

    def __call__(self, scope, receive, send) -> None:
        """Dispatch asgi inject."""
        return self.module.dispatch(scope, receive, send, app=self.app)  # noqa


@dataclass
class Module:
    """Base module."""

    middleware_kw: Dict = field(default_factory=dict)

    __enabled: bool = False
    __app: App = None

    def __call__(self, app: App = None, **kwargs):
        """Call module."""

        with _keep_thread:
            if not app.modules:
                self.app.modules = dict()
            if self.name not in self.app.modules:
                self.app.modules[self.name] = self

        return type(
            f'{self.name.capitalize()}Middleware',
            (InjectMiddleware,),
            {'module': self},
        )

    @property
    def name(self) -> str:
        """Name."""
        return self.__class__.__name__.lower()

    @property
    def enabled(self) -> bool:
        """Is module enabled."""
        return self.__enabled

    @property
    def app(self) -> Optional[App]:
        """App."""
        return self.__app

    @app.setter
    def app(self, new_app: App = None):
        """App."""
        if not self.__app and new_app:
            self.__app = new_app

    async def proceed_message(self, message, scope):
        """Proceed message."""

        if message['type'] == 'lifespan.startup':
            await self.prepare(scope)
            self.__enabled = await self.health(scope)

            if not self.__enabled:
                log.error(
                    f'Module `{self.name}` is not healthy',
                    extra=self.extra_log(),
                )
            else:
                log.debug(f'Module `{self.name}` loaded')

        elif message['type'] == 'lifespan.shutdown':
            await self.release(scope)
        elif message['type'] == 'lifespan.startup.failed':
            self.__enabled = False

    def lifespan(self, scope, receive, send, app: App):
        """On lifespan event."""

        async def dispatch_asgi_hook():
            """Dispatch asgi hook message."""
            log_extra = self.extra_log()
            on_message = await receive()

            if self.app.spec.environment.dont_care_secrets():
                log_extra.update({'scope': scope, 'on_message': on_message})

            try:
                await self.proceed_message(message=on_message, scope=scope)
            except Exception as _exc:
                log.error(
                    f'Module `{self.name}` lifespan, {_exc}',
                    extra=log_extra,
                    exc_info=True,
                )
                raise _exc
            finally:
                return on_message

        return app(scope, dispatch_asgi_hook, send)

    def dispatch(self, scope, receive, send, app: App = None):
        """Process ASGI call."""
        self.app = app
        try:
            if scope['type'] == 'lifespan':
                return self.lifespan(scope, receive, send, app)
            return self.middleware(scope, receive, send, app)
        except Exception as exc:
            log.error(
                f'Dispatch module `{self.name}`, {exc}',
                extra=self.extra_log(add_extra={'scope': scope}),
                exc_info=True,
            )
            raise self.exception(exc, scope, receive, send, app)

    def extra_log(self, add_extra: Dict = None) -> Dict:
        """Extra log."""
        extra = {'module_name': self.name, 'is_enabled': self.enabled}

        if self.app:
            if self.app.spec.environment.dont_care_secrets():
                extra.update({'middleware_kw': self.middleware_kw})
            if self.app.spec.status.debug:
                extra.update({'spec': self.app.spec.as_dict()})

        if add_extra:
            extra.update(add_extra)

        return extra

    def inject(self, app: App) -> None:
        """Set app on start."""
        if self.__app:
            return

        self.__app = app

        _wrapper = self(app=app, **self.middleware_kw)  # noqa
        self.app.add_middleware(_wrapper)

    # Expose

    async def health(self, scope) -> bool:  # noqa
        """Exposer health. Override for own module health check."""
        return True

    async def middleware(self, scope, receive, send, app: App):  # noqa
        """Expose middleware. Override for custom middleware."""
        await app(scope, receive, send)

    async def prepare(self, scope):
        """Expose prepare. Override for prepare module."""
        pass

    async def release(self, scope):
        """Expose release. Override for release module."""
        pass

    def exception(self, exc, scope, receive, send, app: App):  # noqa
        """Expose module exception handling."""
        log_extra = self.extra_log(add_extra={'exc': exc})

        if self.app.spec.environment.dont_care_secrets():
            log_extra.update({'scope': scope})

        log.error(f'Module `{self.name}`, {exc}', extra=log_extra)
        raise exc_type.ModuleException(exc_type)


__all__ = (
    'Router',
    'Route',
    'OpenAPI',
    'get_openapi',
    'Headers',
    'Api',
    'datastructures',
    'Request',
    'Header',
    'Path',
    'Body',
    'Cookie',
    'Query',
    'Depends',
    'Form',
    'File',
    'JSONResponse',
    'UJSONResponse',
    'ORJSONResponse',
    'RedirectResponse',
    'HTMLResponse',
    'StreamingResponse',
    'PlainTextResponse',
    'FileResponse',
    'Response',
    'Middleware',
    'ModuleSettings',
    'UserSettings',
    'Module',
    'InjectMiddleware',
    'Lang',
    'Policies',
    'I18N',
    'Path',
    'URI',
    'Service',
    'ApiDoc',
    'App',
    'Spec',
    'Environment',
    'Status',
    'exc_type',
    'load_spec',
    'PyProject',
)
