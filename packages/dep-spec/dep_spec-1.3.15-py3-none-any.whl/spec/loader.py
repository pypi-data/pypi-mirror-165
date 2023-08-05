"""Loader module."""

from __future__ import annotations

from typing import Dict
from pathlib import Path
from tempfile import gettempdir

from spec import fn
from spec import types

from .exception import PyProjectException, SpecException


def load_uri() -> types.URI:
    """Load service uri."""
    secure = fn.env('service_scheme_secure', cast=str)
    insecure = fn.env('service_scheme_insecure', cast=str)
    scheme = secure if fn.on_k8s() else insecure
    return types.URI(
        host=fn.env('service_host', cast=str),
        port=fn.env('service_port', cast=int),
        scheme=scheme,
    )


def load_service() -> types.Service:
    """Load service."""
    pyproject = fn.load_project_toml()
    poetry: Dict = pyproject.poetry_config

    try:
        return types.Service(
            uri=load_uri(),
            entrypoint=fn.env('service_entrypoint', cast=str),
            name=fn.env('service_name', cast=str),
            tech_name=poetry['name'],
            tech_version=poetry['version'],
            tech_description=poetry.get('description'),
        )
    except Exception as _poetry_exc:
        raise PyProjectException(f'Invalid pyproject.toml poetry section')


def load_status() -> types.Status:
    """Load status."""
    return types.Status(
        debug=fn.env('debug', cast=bool),
        testing=fn.is_testing(),
        on_k8s=fn.on_k8s(),
    )


def load_path() -> types.Path:
    """Load path."""
    assets_dir = Path(fn.app_dir() / 'assets').resolve()

    preferred_assets_dir = fn.env('dir_assets', cast=str)
    if preferred_assets_dir:
        assets_dir = Path(preferred_assets_dir).resolve()

    temp_dir = Path(gettempdir()).resolve()
    preferred_temp_dir = fn.env('dir_temp', cast=str)
    if preferred_temp_dir:
        temp_dir = Path(preferred_temp_dir).resolve()

    log_config_path = fn.env('LOG_CONFIG_PATH', cast=str)
    if not log_config_path or not Path(log_config_path).exists():
        default_log_path = Path(fn.app_dir() / 'log.yaml')
        if default_log_path.exists():
            log_config_path = default_log_path
        else:
            log_config_path = None

    log_config_name = log_config_path.name if log_config_path else None

    return types.Path(
        app=fn.app_dir(),
        assets=assets_dir,
        temp=temp_dir,
        i18n=Path(assets_dir / 'i18n').resolve(),
        static=Path(assets_dir / 'static').resolve(),
        media=Path(assets_dir / 'media').resolve(),
        log_config_name=log_config_name,
        log_config_path=log_config_path,
        pyproject=fn.pyproject_path(),
    )


def load_api_doc() -> types.ApiDoc:
    """Load api doc."""
    return types.ApiDoc(
        enabled=fn.env('APIDOC_ENABLED', cast=bool),
        prefix=fn.env('APIDOC_PREFIX', cast=str),
        blm=fn.env('APIDOC_BLM', cast=bool),
    )


def load_policies() -> types.Policies:
    """Load policies."""
    return types.Policies(
        service_workers=fn.env('policy_service_workers', cast=int),
        db_pool_size=fn.env('policy_db_pool_size', cast=int),
        db_max_connections=fn.env('policy_db_max_connections', cast=int),
        request_timeout=fn.env('policy_request_timeout', cast=int),
        request_retry_max=fn.env('policy_request_retry_max', cast=int),
    )


def load_i18n() -> types.I18N:
    """Load i18n."""

    i18n_lang = fn.env('I18N_LANG', cast=str)
    i18n_support = fn.env('I18N_SUPPORT', cast=list)

    i18n_all = [i18n_lang]
    if i18n_support:
        # support only for foreign enumerations
        assert i18n_lang not in i18n_support
        i18n_all += i18n_support

    return types.I18N(
        lang=i18n_lang,
        support_codes=i18n_support or list(),
        all_codes=i18n_all,
        locales=fn.env('I18N_LOCALES', cast=list),
    )

def load_profile() -> types.Profile:
    """Load profile."""
    return types.Profile(
        sentry_dsn=fn.sentry_dsn(),
        log_level=fn.env('LOG_LEVEL', cast=str),
    )


def load_spec() -> types.Spec:
    """Load spec."""
    try:
        return types.Spec(
            environment=types.Environment(fn.environment_plain()),  # noqa
            pyproject=fn.load_project_toml(),
            service=load_service(),
            status=load_status(),
            path=load_path(),
            policies=load_policies(),
            api_doc=load_api_doc(),
            i18n=load_i18n(),
            profile=load_profile(),
        )
    except Exception as _spec_exception:
        raise SpecException(_spec_exception)
