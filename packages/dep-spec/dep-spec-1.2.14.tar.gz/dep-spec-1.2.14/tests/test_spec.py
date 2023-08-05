"""Spec testing."""

import os

from pathlib import Path
from tempfile import gettempdir

from spec import Spec, default, fn, types, load_spec


def test_defaults(default_spec):
    """Test defaults values."""
    for (alias, cast_type, right_value) in default_spec:
        eval_value = fn.env(alias, cast=cast_type)
        assert eval_value == right_value


def test_as_dict(mock_pyproject_path):
    """Test as dict."""
    spec = load_spec()
    as_dict = spec.as_dict()
    as_dict_keys = (
        'service',
        'status',
        'path',
        'policies',
        'i18n',
        'api_doc',
        'profile',
    )

    for dict_key in as_dict_keys:
        assert dict_key in as_dict.keys()


def test_spec_with_defaults(mock_pyproject_path):
    """Test spec with default values."""

    spec = load_spec()

    assert isinstance(spec, Spec)

    assert spec.api_doc.enabled
    assert spec.api_doc.prefix == '/doc'
    assert not spec.api_doc.blm

    assert spec.profile.log_level == default.get('LOG_LEVEL')
    assert spec.profile.sentry_dsn == default.get('SENTRY_DSN')

    assert spec.service.uri == types.URI(
        host=default.get('SERVICE_HOST'),
        port=default.get('SERVICE_PORT'),
        scheme=default.get('SERVICE_SCHEME_INSECURE'),
    )

    assert spec.service == types.Service(
        name=default.get('SERVICE_NAME'),
        entrypoint=default.get('SERVICE_ENTRYPOINT'),
        uri=spec.service.uri,
        tech_name='dep-spec',
        tech_version='1.2.3',
        tech_description='Spec description',
    )

    assert spec.policies == types.Policies(
        service_workers=default.get('POLICY_SERVICE_WORKERS'),
        db_pool_size=default.get('POLICY_DB_POOL_SIZE'),
        db_max_connections=default.get('POLICY_DB_MAX_CONNECTIONS'),
        request_timeout=default.get('POLICY_REQUEST_TIMEOUT'),
        request_retry_max=default.get('POLICY_REQUEST_RETRY_MAX'),
    )

    assert spec.path == types.Path(
        app=Path(os.getcwd()).resolve(),
        temp=Path(gettempdir()).resolve(),
        assets=Path(spec.path.app / 'assets').resolve(),
        i18n=Path(spec.path.assets / 'i18n').resolve(),
        media=Path(spec.path.assets / 'media').resolve(),
        static=Path(spec.path.assets / 'static').resolve(),
        pyproject=mock_pyproject_path,
        log_config_name=None,
        log_config_path=None,
    )

    all_codes = [default.get('I18N_LANG')]
    all_codes += default.get('I18N_SUPPORT')

    assert spec.i18n == types.I18N(
        lang=default.get('I18N_LANG'),
        support_codes=default.get('I18N_SUPPORT'),
        locales=default.get('I18N_LOCALES'),
        all_codes=all_codes,
    )

    assert spec.status == types.Status(
        debug=default.get('DEBUG'),
        testing=fn.is_testing(),
        on_k8s=fn.on_k8s(),
    )


def test_k8s_on(mock_pyproject_path, k8s_running):  # noqa
    """Test spec with default values."""

    assert fn.on_k8s()

    spec = load_spec()
    assert spec.status.on_k8s
