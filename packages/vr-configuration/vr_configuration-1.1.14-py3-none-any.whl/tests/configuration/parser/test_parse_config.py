from pathlib import Path

from pytest import fixture
from pytest import raises

from vr_configuration.parser.config_parsing import parse_config
from vr_configuration.paths import CONFIG_PATH
from vr_configuration.printing.recursive_dumping import \
    dump_recursively


@fixture
def config_string() -> str:
    config_string: str = """Config:
    greetee: World
    greeting: Hello
"""

    return config_string


@fixture
def subconfig_string() -> str:
    subconfig_string: str = """Config:
    SubConfig:
        greetee: World
    greeting: Hello
"""

    return subconfig_string


def test_parse_config(config_string):
    # Test
    config: type = parse_config(
        config_file_path=CONFIG_PATH / "config.yaml",
    )

    # Assert
    assert isinstance(config, type)

    string: str = dump_recursively(obj=config)

    assert string == config_string


def test_parse_config_multiple_roots():
    # Mock
    config_file_path: Path = CONFIG_PATH / 'config_multiple_roots.yaml'

    # Assert
    with raises(NotImplementedError):

        # Test
        _ = parse_config(
            config_file_path=config_file_path,
        )


def test_parse_config_subconfig(subconfig_string):
    # Mock
    config_file_path: Path = CONFIG_PATH / 'config_subconfig.yaml'

    # Test
    config: type = parse_config(
        config_file_path=config_file_path,
    )

    # Assert
    assert isinstance(config, type)

    string: str = dump_recursively(obj=config)

    assert string == subconfig_string
