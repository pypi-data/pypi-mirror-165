from typing import List, Optional

from vr_configuration.hello_world.punctuation_enum import PunctuationEnum

from vr_configuration.parser.enumeration_parsing import parse_enum


def parse_punctuation(ConfigPunctuation) -> type:
    attribute_path: Optional[List[str]] = None
    attribute_name: str = 'punctuation'

    parse_enum(
        config=ConfigPunctuation,
        attribute_path=attribute_path,
        attribute_name=attribute_name,
        enum=PunctuationEnum,
    )

    return ConfigPunctuation
