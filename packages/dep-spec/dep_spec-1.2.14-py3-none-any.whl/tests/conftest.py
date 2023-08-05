"""Conftest."""

import pytest

from typing import Any, Sequence, TypeVar, Tuple

from pathlib import Path

from spec import fn
from spec.types import App, Spec
from spec.loader import load_spec
from spec.default import get


@pytest.fixture
def default_spec() -> Sequence[Tuple[str, TypeVar, Any]]:
    """Spec default values."""
    return (
        ('ENVIRONMENT', str, get('ENVIRONMENT')),
        ('SERVICE_HOST', str, get('SERVICE_HOST')),
        ('SERVICE_PORT', int, get('SERVICE_PORT')),
        ('SERVICE_NAME', str, get('SERVICE_NAME')),
        ('SERVICE_SCHEME_SECURE', str, get('SERVICE_SCHEME_SECURE')),
        ('SERVICE_SCHEME_INSECURE', str, get('SERVICE_SCHEME_INSECURE')),
        ('LOG_LEVEL', str, get('LOG_LEVEL')),
        ('LOG_CONFIG_PATH', str, get('LOG_CONFIG_PATH')),
        ('ENV_FILE', str, get('ENV_FILE')),
        ('SENTRY_DSN', str, get('SENTRY_DSN')),
        ('POLICY_SERVICE_WORKERS', str, get('POLICY_SERVICE_WORKERS')),
        ('POLICY_REQUEST_TIMEOUT', str, get('POLICY_REQUEST_TIMEOUT')),
        ('POLICY_REQUEST_RETRY', str, get('POLICY_REQUEST_RETRY')),
        ('POLICY_SCHEDULER_ENABLED', str, get('POLICY_SCHEDULER_ENABLED')),
        ('POLICY_SCHEDULER_PERSISTENT', str, get('POLICY_SCHEDULER_PERSISTENT')),
        ('POLICY_SCHEDULER_WORKERS', str, get('POLICY_SCHEDULER_WORKERS')),
        ('POLICY_SCHEDULER_INSTANCES', str, get('POLICY_SCHEDULER_INSTANCES')),
        ('POLICY_SCHEDULER_HOST', str, get('POLICY_SCHEDULER_HOST')),
        ('POLICY_SCHEDULER_PORT', str, get('POLICY_SCHEDULER_PORT')),
        ('POLICY_SCHEDULER_DB', str, get('POLICY_SCHEDULER_DB')),
        ('POLICY_SCHEDULER_COALESCE', str, get('POLICY_SCHEDULER_COALESCE')),
        ('I18N_LANG', str, get('I18N_LANG')),
        ('I18N_SUPPORT', str, get('I18N_SUPPORT')),
        ('I18N_LOCALES', str, get('I18N_LOCALES')),
    )


@pytest.fixture
def k8s_running(mocker):
    """Mock k8s running."""
    mocker.patch('spec.fn.on_k8s', return_value=True)


@pytest.fixture
def env_sentry_dsn(monkeypatch) -> str:
    """Mock k8s running."""
    dsn = 'https://valid.sentry.dsn'
    monkeypatch.setenv('SENTRY_DSN', dsn)
    yield dsn
    monkeypatch.delenv('SENTRY_DSN', raising=False)


@pytest.fixture
def mock_pyproject_path(mocker) -> Path:
    """Pyproject path."""
    mocker.patch(
        'spec.fn.pyproject_path',
        return_value=Path(fn.app_dir() / 'tests' / 'mock.toml')
    )
    return fn.pyproject_path()


@pytest.fixture
def spec() -> Spec:
    """Mock spec."""
    _spec = load_spec()
    yield _spec


@pytest.fixture
def app(spec) -> App:
    """Mock app."""

    from spec.types import App, JSONResponse

    app = App()
    app.spec = spec

    @app.route('/')
    async def home(request):  # noqa
        return JSONResponse({'status': 'ok'})

    yield app


@pytest.fixture
def client(app):
    """Mock client."""
    from fastapi.testclient import TestClient
    return TestClient(app)
