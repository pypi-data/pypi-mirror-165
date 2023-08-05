from enum import Enum
from typing import Any, List, Type, Optional

from vr_configuration.parser._sub_config_getting import _get_subconfig


def parse_enum(
    *,
    config: Any,
    attribute_path: Optional[List[str]],
    attribute_name: str,
    enum: Type[Enum],
) -> None:
    """
    Parse enumerations in a configuration object.

    After calling this function, the parsed value of the enumeration type will
    be stored in the configuration object at the given path in an attribute
    with the given name.

    :param config: The config object to parse enumerations in.
    :param attribute_path: The path of the attribute containing an enumeration.
    :param attribute_name: The name of the attribute containing an enumeration.
    :param enum: The enumeration type to be parsed from the attribute value.

    :return None
    """
    config = _get_subconfig(
        config=config,
        attribute_path=attribute_path,
    )

    attribute_value_string: type = getattr(config, attribute_name)

    found = False
    for enum_attribute in enum:
        if attribute_value_string == str(enum_attribute):
            target_value = getattr(enum, str(enum_attribute).split('.')[1])
            setattr(config, attribute_name, target_value)
            found = True

    if not found:
        raise NotImplementedError(
            f'The string value {attribute_value_string} does not match any '
            f'attribute names in the enumeration {enum}.'
        )
