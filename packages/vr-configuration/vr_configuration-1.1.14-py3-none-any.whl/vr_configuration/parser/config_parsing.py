from pathlib import Path

import yaml

from vr_configuration.parser._create_potentially_nested_type \
    import _create_potentially_nested_type


def parse_config(
    *,
    config_file_path: Path,
) -> type:
    """
    Parse a config yaml file to Python class hierarchy with attributes.

    :param config_file_path: The config file to parse

    :return: A type hierarchy with the configured values in the attributes.
    """
    with open(config_file_path, "r") as stream:
        config_dict: dict = yaml.safe_load(stream=stream)

        if list(config_dict.keys())[0] != 'Config':
            raise NotImplementedError(
                f'Can only parse objects of type config, '
                f'but got object of type {list(config_dict.keys())[0]}'
            )

    config: type = _create_potentially_nested_type(
        attribute_value=config_dict,
    )

    return config
