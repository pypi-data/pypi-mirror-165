# The first definition is for the structure and type hints.
# The second definition is for loading the vr_configuration values.
from vr_configuration.paths import CONFIG_PATH
from vr_configuration.parser.config_parsing import parse_config


class Config:
    greeting: str
    greetee: str


Config: type = parse_config(  # type: ignore # noqa
    config_file_path=CONFIG_PATH / 'config.yaml',
)
