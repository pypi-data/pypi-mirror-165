"""Test versions."""

from spec import fn


def test_reading_spec(mock_pyproject_path):
    """Test spec version."""

    assert fn.version() == '1.2.3'

    pyproject = fn.load_project_toml()

    config = pyproject.poetry_config

    assert config['name'] == 'dep-spec'
    assert config['version'] == fn.version()

    check_deps = {'python': '^3.9', 'fastapi': '^0.79.0'}
    for _dep, _ver in check_deps.items():
        assert config['dependencies'][_dep] == _ver
