"""Test socket."""

from spec import load_spec


def test_socket_overload_insecure(
    mock_pyproject_path,  # noqa
    monkeypatch,
):
    """Test sentry on k8s and not testing environment."""

    monkeypatch.setenv('SERVICE_HOST', '127.0.0.1')
    monkeypatch.setenv('SERVICE_PORT', '7070')

    spec = load_spec()

    assert spec.service.uri.host == '127.0.0.1'
    assert spec.service.uri.port == 7070
    assert spec.service.uri.scheme == 'http'


def test_socket_overload_secure(
    mock_pyproject_path,  # noqa
    k8s_running,
    monkeypatch,
):
    """Test sentry on k8s and not testing environment."""

    monkeypatch.setenv('SERVICE_HOST', '127.0.0.2')
    monkeypatch.setenv('SERVICE_PORT', '9090')

    spec = load_spec()

    assert spec.service.uri.host == '127.0.0.2'
    assert spec.service.uri.port == 9090
    assert spec.service.uri.scheme == 'https'
