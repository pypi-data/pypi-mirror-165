"""Testing sentry."""

from spec import load_spec


def test_sentry_default(mock_pyproject_path, env_sentry_dsn, monkeypatch):  # noqa
    """Test not sentry with unknown env not on k8s."""
    spec = load_spec()
    assert not spec.status.on_k8s
    assert not spec.profile.sentry_dsn


def test_sentry_local_disabled(mock_pyproject_path, env_sentry_dsn, monkeypatch):  # noqa
    """Test sentry not on k8s and not testing environment."""
    monkeypatch.setenv('ENVIRONMENT', 'develop')
    spec = load_spec()
    assert not spec.status.on_k8s
    assert not spec.profile.sentry_dsn


def test_sentry_k8s_enabled(
    mock_pyproject_path,  # noqa
    k8s_running,  # noqa
    env_sentry_dsn,  # noqa
    monkeypatch,
):
    """Test sentry on k8s and not testing environment."""
    monkeypatch.setenv('ENVIRONMENT', 'develop')
    spec = load_spec()
    assert spec.status.on_k8s
    assert spec.profile.sentry_dsn
