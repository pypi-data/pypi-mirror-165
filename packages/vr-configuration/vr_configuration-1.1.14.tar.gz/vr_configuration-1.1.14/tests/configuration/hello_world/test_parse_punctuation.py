from pathlib import Path
from typing import Optional, List

from pytest import raises

from vr_configuration.hello_world.parse_punctuation import parse_punctuation
from vr_configuration.parser.enumeration_parsing import parse_enum
from vr_configuration.hello_world.punctuation_enum import PunctuationEnum
from vr_configuration.parser.config_parsing import parse_config
from vr_configuration.paths import CONFIG_PATH


def test_parse_punctuation_dot():
    # Mock
    config_file_path: Path = \
        CONFIG_PATH / 'config_with_punctuation_dot.yaml'
    ConfigPunctuation: type = parse_config(  # type: ignore # noqa
        config_file_path=config_file_path,
    )

    # Test
    parse_punctuation(ConfigPunctuation)

    # Assert
    assert ConfigPunctuation.punctuation
    assert isinstance(ConfigPunctuation.punctuation, PunctuationEnum)
    assert ConfigPunctuation.punctuation == PunctuationEnum.Dot


def test_parse_punctuation_exclamation_mark():
    # Mock
    config_file_path: Path = \
        CONFIG_PATH / 'config_with_punctuation_exclamation_mark.yaml'
    ConfigPunctuation: type = parse_config(  # type: ignore # noqa
        config_file_path=config_file_path,
    )

    # Test
    parse_punctuation(ConfigPunctuation)

    # Assert
    assert ConfigPunctuation.punctuation
    assert isinstance(ConfigPunctuation.punctuation, PunctuationEnum)
    assert ConfigPunctuation.punctuation == PunctuationEnum.ExclamationMark


def test_parse_punctuation_question_mark():
    # Mock
    config_file_path: Path = \
        CONFIG_PATH / 'config_with_punctuation_question_mark.yaml'
    ConfigPunctuation: type = parse_config(  # type: ignore # noqa
        config_file_path=config_file_path,
    )

    # Test
    parse_punctuation(ConfigPunctuation)

    # Assert
    assert ConfigPunctuation.punctuation
    assert isinstance(ConfigPunctuation.punctuation, PunctuationEnum)
    assert ConfigPunctuation.punctuation == PunctuationEnum.QuestionMark


def test_parse_punctuation_not_implemented():
    # Mock
    config_file_path: Path = \
        CONFIG_PATH / 'config_with_punctuation_not_implemented.yaml'
    ConfigPunctuation: type = parse_config(  # type: ignore # noqa
        config_file_path=config_file_path,
    )

    # Assert
    with raises(NotImplementedError):
        # Test
        parse_punctuation(ConfigPunctuation)


def test_parse_punctuation_dot_subconfig():
    # Mock
    config_file_path: Path = \
        CONFIG_PATH / 'config_with_punctuation_dot_subconfig.yaml'
    ConfigPunctuation: type = parse_config(  # type: ignore # noqa
        config_file_path=config_file_path,
    )
    attribute_path: Optional[List[str]] = ['SubConfig']
    attribute_name: str = 'punctuation'

    # Test
    parse_enum(
        config=ConfigPunctuation,
        attribute_path=attribute_path,
        attribute_name=attribute_name,
        enum=PunctuationEnum,
    )

    # Assert
    assert ConfigPunctuation.SubConfig.punctuation
    assert isinstance(
        ConfigPunctuation.SubConfig.punctuation,
        PunctuationEnum,
    )
    assert ConfigPunctuation.SubConfig.punctuation == \
           PunctuationEnum.Dot
