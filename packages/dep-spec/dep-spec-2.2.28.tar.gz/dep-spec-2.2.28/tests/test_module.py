"""Test modules."""

import asyncio

from dataclasses import dataclass
from asgi_lifespan import LifespanManager
from logging import CRITICAL
from pytest import fixture
from unittest.mock import Mock

from spec.types import Module as TypeModule
from spec.ext.testing import AppClient


check = Mock()
check_broken = Mock()


@fixture
def module():
    """Mock test module."""

    @dataclass
    class Module(TypeModule):
        """Test module."""

        uri: str = 'any'

        async def prepare(self, scope):  # noqa
            """Test prepare hook."""
            check('lifespan', 'startup')

        async def release(self, scope):  # noqa
            """Test release hook."""
            check('lifespan', 'shutdown')

        async def middleware(self, scope, receive, send, app=None):  # noqa
            """Test http middleware."""
            check('middleware', self.name, scope['type'])
            return await app(scope, receive, send)

    yield Module()


@fixture
def broken_module():
    """Mock test broken module."""

    @dataclass
    class BrokenModule(TypeModule):
        """Test  broken module."""

        async def prepare(self, scope):  # noqa
            """Test prepare hook."""
            check_broken('lifespan', 'startup')
            1 / 0  # noqa

        async def release(self, scope):  # noqa
            """Test release hook."""
            check_broken('lifespan', 'shutdown')

    yield BrokenModule()


@fixture
def unhealthy_module():
    """Mock unhealthy module."""

    @dataclass
    class UnhealthyModule(TypeModule):
        """Test module."""

        uri: str = 'any'

        async def prepare(self, scope):  # noqa
            """Test prepare hook."""
            check('lifespan', 'startup')

        async def release(self, scope):  # noqa
            """Test release hook."""
            check('lifespan', 'shutdown')

        async def health(self, scope) -> bool:
            """Set false for test."""
            return False

        async def middleware(self, scope, receive, send, app=None):  # noqa
            """Test http middleware."""
            check('middleware', self.name, scope['type'])
            return await app(scope, receive, send)

    yield UnhealthyModule()


@fixture
def client(app) -> AppClient:
    """Mock client."""
    return AppClient(app=app)


def test_smoke(app, module):
    """Smoke module tests."""

    assert module.name == 'module'
    assert not module.app
    assert not module.enabled

    module.inject(app)
    assert module.app is app


def test_asgi_lifespan(client, module):
    """Test module with async asgi lifespan."""
    module.inject(app=client.app)

    async def emulate_lifespan():
        """Lifespan."""

        async with LifespanManager(client.app):

            assert module.enabled
            assert client.app.modules['module'] is module

            with client:
                res = client.get('/')
                assert res.status_code == 200

            assert [args[0] for args in check.call_args_list] == [
                ('lifespan', 'startup'),  # module call
                ('lifespan', 'startup'),  # middleware call
                ('middleware', 'module', 'http'),  # request call
                ('lifespan', 'shutdown'),  # bye
            ]

    asyncio.run(emulate_lifespan())


async def test_broken(client, broken_module, caplog):
    """Test disabled module with preparing errors."""

    caplog.set_level(CRITICAL)
    broken_module.inject(app=client.app)

    async with LifespanManager(client.app):
        assert not broken_module.enabled

        with client:
            res = client.get('/')
            assert res.status_code == 200

        assert [args[0] for args in check_broken.call_args_list] == [
            ('lifespan', 'startup'),  # module
            ('lifespan', 'startup'),  # middleware
            ('lifespan', 'shutdown'),
        ]


async def test_un_health(client, unhealthy_module, caplog):
    """Test disabled by health check."""

    caplog.set_level(CRITICAL)
    unhealthy_module.inject(app=client.app)

    async with LifespanManager(client.app):
        assert not unhealthy_module.enabled
