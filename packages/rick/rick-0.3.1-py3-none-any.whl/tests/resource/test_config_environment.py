import os
import pytest
from rick.resource.config import EnvironmentConfig

class ConfigTest1(EnvironmentConfig):
    OPTION_1 = None
    OPTION_2 = 'x'


fixture_configtest1 = [(ConfigTest1, {'OPTION_1': 'abc', 'OPTION_2': 'def'})]

@pytest.mark.parametrize("fixture", fixture_configtest1)
def test_ConfigEnvironment(fixture):
    for name, value in fixture[1].items():
        os.environ[name] = str(value)

    # build config object
    cfg = fixture[0]()

    # check if values were overridden
    for name, value in fixture[1].items():
        assert getattr(cfg, name) == str(value)

fixture_configtest_prefix = [(ConfigTest1, {'PREFIX_OPTION_1': 'abc', 'PREFIX_OPTION_2': 'def'})]

@pytest.mark.parametrize("fixture", fixture_configtest_prefix)
def test_ConfigEnvironment_prefix(fixture):
    for name, value in fixture[1].items():
        os.environ[name] = str(value)

    # build config object
    prefix = 'PREFIX_'
    cfg = fixture[0](prefix)

    # check if values were overridden
    for name, value in fixture[1].items():
        assert getattr(cfg, name.replace(prefix, '')) == str(value)

