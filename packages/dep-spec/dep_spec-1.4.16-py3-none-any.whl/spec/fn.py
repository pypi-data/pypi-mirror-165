"""Fn module."""

import os
import sys

from dotenv import load_dotenv
from logging import getLogger
from poetry.core.pyproject import PyProjectTOML as PyProject
from typing import Any, TypeVar, Optional
from spec import default as spec_default
from pathlib import Path

from .exception import PyProjectException


log = getLogger(__name__)


def app_dir() -> Path:
    """App dir."""
    return Path(os.getcwd()).resolve()


def pyproject_path() -> Path:
    """Pyproject path."""
    return Path(app_dir() / 'pyproject.toml').resolve()


def env(alias: str, cast: TypeVar) -> Any:
    """Try env or try default or none."""
    name = str(alias).upper()
    if name in os.environ.keys():
        env_val = os.environ.get(name)
        if env_val is None:
            return None
        if isinstance(cast, list):
            return str(env_val).split(' ')
        return cast(env_val)
    return spec_default.get(name)


def load_env():
    """Load env."""
    env_path = Path(os.getcwd()).resolve() / env('env_file', cast=str)
    if env_path.exists():
        load_dotenv(env_path.as_posix())


def _found_testing_modules() -> bool:
    """Found unittests/pytest modules runtime."""
    loaded_modules = sys.modules.keys()
    modules = (
        '_pytest' in loaded_modules,
        'unittest' in loaded_modules,
    )
    return any(modules)


def is_testing() -> bool:
    """Is testing currently."""
    return any([
        _found_testing_modules(),
        env('ENVIRONMENT', cast=str) == 'testing',
    ])


def on_k8s() -> bool:
    """if running under kubernetes"""
    return any([
        True if str(_opt).upper().startswith('KUBERNETES') else False
        for _opt in os.environ.keys()
    ])


def environment_plain() -> str:
    """Load environment plain."""
    return str(os.environ.get('ENVIRONMENT', 'unknown')).lower()


def sentry_dsn() -> Optional[str]:
    """Sentry dsn."""
    if env('environment', cast=str) in ('testing', 'unknown'):
        return
    elif not on_k8s():
        return
    return env('SENTRY_DSN', cast=str)


def locale_dot_gen() -> Path:
    """Get locale.gen file."""
    return Path(app_dir() / 'locale.gen').resolve()


def load_project_toml() -> PyProject:
    """Load project toml."""

    try:
        project_toml = PyProject(pyproject_path())
    except Exception as _load_exc:
        raise PyProjectException(_load_exc)

    if not project_toml.is_poetry_project():
        raise PyProjectException('Is not poetry project')

    return project_toml


def version() -> str:
    """Spec version."""

    pyproject = load_project_toml()
    assert pyproject.poetry_config['name'] == 'dep-spec'
    return pyproject.poetry_config['version']
