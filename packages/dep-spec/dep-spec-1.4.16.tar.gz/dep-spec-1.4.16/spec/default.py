"""Spec defaults."""

from typing import Any, Union


_OPTIONS_DEFAULT = {
    'SERVICE_NAME': 'Service',
    'SERVICE_HOST': '0.0.0.0',
    'SERVICE_PORT': 6969,
    'SERVICE_ENTRYPOINT': 'main:app',
    'SERVICE_SCHEME_SECURE': 'https',
    'SERVICE_SCHEME_INSECURE': 'http',

    'ENV_FILE': '.env',
    'ENVIRONMENT': 'unknown',
    'DEBUG': False,

    'LOG_LEVEL': 'debug',

    'LOG_CONFIG_PATH': None,

    'SENTRY_DSN': None,
    'DIR_ASSETS': None,

    # Policies

    'POLICY_SERVICE_WORKERS': 1,

    'POLICY_DB_POOL_SIZE': 5,
    'POLICY_DB_MAX_CONNECTIONS': 10,

    'POLICY_REQUEST_TIMEOUT': 60,
    'POLICY_REQUEST_RETRY_MAX': 3,

    'POLICY_SCHEDULER_ENABLED': False,
    'POLICY_SCHEDULER_PERSISTENT': False,
    'POLICY_SCHEDULER_WORKERS': 1,
    'POLICY_SCHEDULER_INSTANCES': 5,
    'POLICY_SCHEDULER_HOST': 'localhost',
    'POLICY_SCHEDULER_PORT': 6379,
    'POLICY_SCHEDULER_DB': 9,
    'POLICY_SCHEDULER_COALESCE': False,

    'APIDOC_ENABLED': True,
    'APIDOC_PREFIX': '/doc',
    'APIDOC_BLM': False,

    'I18N_LANG': 'en',
    'I18N_SUPPORT': ['ru'],
    'I18N_LOCALES': ['en_US', 'ru_RU'],
}


def get(alias: str) -> Union[Any, None]:
    """Get default for spec"""
    return _OPTIONS_DEFAULT.get(str(alias).upper(), None)
